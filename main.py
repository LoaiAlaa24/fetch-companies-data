from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from contextlib import contextmanager

# Database configuration
DB_CONFIG = {
    'host': os.getenv('PGHOST', 'localhost'),
    'port': int(os.getenv('PGPORT', 5432)),
    'database': os.getenv('PGDATABASE', 'your_database'),
    'user': os.getenv('PGUSER', 'postgres'),
    'password': os.getenv('PGPASSWORD', 'your_password')
}

TABLE_NAME = 'european_companies'

# Initialize FastAPI app
app = FastAPI(
    title="European Companies API",
    description="Lightweight API to query European companies by domain",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Response models
class Company(BaseModel):
    id: int
    country: Optional[str]
    founded: Optional[str]
    company_id: str
    industry: Optional[str]
    linkedin_url: Optional[str]
    locality: Optional[str]
    name: Optional[str]
    region: Optional[str]
    size: Optional[str]
    website: Optional[str]

class CompanyResponse(BaseModel):
    success: bool
    data: Optional[Company]
    message: Optional[str]

class CompaniesListResponse(BaseModel):
    success: bool
    data: List[Company]
    count: int
    message: Optional[str]

# Database context manager
@contextmanager
def get_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

# Utility function to extract domain from website
def extract_domain(website: str) -> str:
    """Extract domain from website URL"""
    if not website:
        return ""

    # Remove protocol
    domain = website.replace('http://', '').replace('https://', '')

    # Remove www.
    domain = domain.replace('www.', '')

    # Remove path and query parameters
    domain = domain.split('/')[0].split('?')[0]

    return domain.lower().strip()

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "European Companies API",
        "version": "1.0.0",
        "endpoints": {
            "/health": "Health check",
            "/company/domain/{domain}": "Get company by domain",
            "/companies/search": "Search companies",
            "/stats": "Get database statistics"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")

@app.get("/company/domain/{domain}", response_model=CompanyResponse)
async def get_company_by_domain(domain: str):
    """
    Get company information by domain name

    Example: /company/domain/example.com
    """
    try:
        # Clean the domain
        clean_domain = extract_domain(domain)

        if not clean_domain:
            raise HTTPException(status_code=400, detail="Invalid domain")

        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            # Search for company with matching domain
            query = f"""
                SELECT * FROM {TABLE_NAME}
                WHERE LOWER(REPLACE(REPLACE(REPLACE(website, 'http://', ''), 'https://', ''), 'www.', ''))
                LIKE %s
                LIMIT 1;
            """

            cursor.execute(query, (f"{clean_domain}%",))
            result = cursor.fetchone()
            cursor.close()

            if result:
                return CompanyResponse(
                    success=True,
                    data=Company(**result),
                    message="Company found"
                )
            else:
                raise HTTPException(status_code=404, detail=f"No company found for domain: {domain}")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/companies/search", response_model=CompaniesListResponse)
async def search_companies(
    country: Optional[str] = Query(None, description="Filter by country"),
    name: Optional[str] = Query(None, description="Search by company name"),
    industry: Optional[str] = Query(None, description="Filter by industry"),
    limit: int = Query(10, ge=1, le=100, description="Number of results to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination")
):
    """
    Search companies with filters

    Example: /companies/search?country=germany&limit=20
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            # Build query dynamically
            conditions = []
            params = []

            if country:
                conditions.append("LOWER(country) = LOWER(%s)")
                params.append(country)

            if name:
                conditions.append("LOWER(name) LIKE LOWER(%s)")
                params.append(f"%{name}%")

            if industry:
                conditions.append("LOWER(industry) LIKE LOWER(%s)")
                params.append(f"%{industry}%")

            where_clause = " AND ".join(conditions) if conditions else "1=1"

            query = f"""
                SELECT * FROM {TABLE_NAME}
                WHERE {where_clause}
                ORDER BY name
                LIMIT %s OFFSET %s;
            """

            params.extend([limit, offset])
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()

            companies = [Company(**row) for row in results]

            return CompaniesListResponse(
                success=True,
                data=companies,
                count=len(companies),
                message=f"Found {len(companies)} companies"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/stats")
async def get_statistics():
    """Get database statistics"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            # Total companies
            cursor.execute(f"SELECT COUNT(*) as total FROM {TABLE_NAME};")
            total = cursor.fetchone()['total']

            # Companies by country
            cursor.execute(f"""
                SELECT country, COUNT(*) as count
                FROM {TABLE_NAME}
                GROUP BY country
                ORDER BY count DESC
                LIMIT 10;
            """)
            countries = cursor.fetchall()

            # Companies by size
            cursor.execute(f"""
                SELECT size, COUNT(*) as count
                FROM {TABLE_NAME}
                WHERE size IS NOT NULL
                GROUP BY size
                ORDER BY count DESC;
            """)
            sizes = cursor.fetchall()

            cursor.close()

            return {
                "success": True,
                "total_companies": total,
                "top_countries": countries,
                "company_sizes": sizes
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
