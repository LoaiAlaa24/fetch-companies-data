# European Companies API

A lightweight FastAPI service to query European company data by domain/website.

## Features

- **Fast domain lookup**: Get company information by website domain
- **Search & filter**: Search companies by country, name, or industry
- **Statistics**: Get database statistics and insights
- **CORS enabled**: Ready for frontend integration
- **Health checks**: Monitor API and database status

## Installation

```bash
cd api
pip install -r requirements.txt
```

## Running the API

```bash
# Development mode (with auto-reload)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at: `http://localhost:8000`

## API Endpoints

### 1. Get Company by Domain

Get company information by website domain.

```bash
GET /company/domain/{domain}

# Examples:
curl http://localhost:8000/company/domain/example.com
curl http://localhost:8000/company/domain/google.de
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 123,
    "country": "germany",
    "founded": "2010",
    "company_id": "abc123",
    "industry": "technology",
    "linkedin_url": "linkedin.com/company/example",
    "locality": "berlin",
    "name": "Example GmbH",
    "region": "berlin",
    "size": "51-200",
    "website": "example.com"
  },
  "message": "Company found"
}
```

### 2. Search Companies

Search and filter companies with pagination.

```bash
GET /companies/search

# Query parameters:
# - country: Filter by country (e.g., "germany", "france")
# - name: Search by company name
# - industry: Filter by industry
# - limit: Number of results (default: 10, max: 100)
# - offset: Pagination offset (default: 0)

# Examples:
curl "http://localhost:8000/companies/search?country=germany&limit=20"
curl "http://localhost:8000/companies/search?name=tech&industry=software"
curl "http://localhost:8000/companies/search?country=france&offset=20&limit=10"
```

**Response:**
```json
{
  "success": true,
  "data": [...],
  "count": 20,
  "message": "Found 20 companies"
}
```

### 3. Get Statistics

Get database statistics.

```bash
GET /stats

curl http://localhost:8000/stats
```

**Response:**
```json
{
  "success": true,
  "total_companies": 6997121,
  "top_countries": [
    {"country": "united kingdom", "count": 1500000},
    {"country": "germany", "count": 1200000}
  ],
  "company_sizes": [
    {"size": "1-10", "count": 3000000},
    {"size": "11-50", "count": 2000000}
  ]
}
```

### 4. Health Check

Check API and database health.

```bash
GET /health

curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

## Interactive API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Environment Variables

Create a `.env` file in the `api/` directory (copy from `.env.example`):

```bash
cp .env.example .env
```

Then edit `.env` with your database credentials:

```bash
PGHOST=your_database_host
PGPORT=5432
PGDATABASE=your_database_name
PGUSER=your_database_user
PGPASSWORD=your_database_password
```

**Note**: The `.env` file should never be committed to version control. It's already included in `.gitignore`.

## Example Usage with Python

```python
import requests

# Get company by domain
response = requests.get("http://localhost:8000/company/domain/example.com")
company = response.json()

if company['success']:
    print(f"Company: {company['data']['name']}")
    print(f"Country: {company['data']['country']}")
    print(f"Website: {company['data']['website']}")

# Search companies
response = requests.get(
    "http://localhost:8000/companies/search",
    params={"country": "germany", "limit": 50}
)
companies = response.json()
print(f"Found {companies['count']} German companies")
```

## Example Usage with cURL

```bash
# Get company by domain
curl -X GET "http://localhost:8000/company/domain/example.com" | jq

# Search German tech companies
curl -X GET "http://localhost:8000/companies/search?country=germany&industry=technology&limit=10" | jq

# Get statistics
curl -X GET "http://localhost:8000/stats" | jq
```

## Deployment

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t european-companies-api .
docker run -p 8000:8000 european-companies-api
```

### Railway/Heroku Deployment

Add a `Procfile`:

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

## Performance Tips

- Use pagination for large result sets
- Consider adding caching (Redis) for frequently accessed domains
- Use connection pooling for database connections
- Deploy with multiple workers in production

## License

MIT
