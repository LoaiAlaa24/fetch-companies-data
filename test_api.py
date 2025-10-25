#!/usr/bin/env python3
"""
Simple test script for the European Companies API
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("\n" + "="*60)
    print("Testing Health Endpoint")
    print("="*60)

    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    return response.status_code == 200

def test_get_company_by_domain(domain):
    """Test getting company by domain"""
    print("\n" + "="*60)
    print(f"Testing Get Company by Domain: {domain}")
    print("="*60)

    response = requests.get(f"{BASE_URL}/company/domain/{domain}")
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        if data['success']:
            company = data['data']
            print(f"\nCompany Found:")
            print(f"  Name:     {company.get('name')}")
            print(f"  Country:  {company.get('country')}")
            print(f"  Website:  {company.get('website')}")
            print(f"  Industry: {company.get('industry')}")
            print(f"  Size:     {company.get('size')}")
            print(f"  LinkedIn: {company.get('linkedin_url')}")
            return True
    else:
        print(f"Response: {json.dumps(response.json(), indent=2)}")

    return False

def test_search_companies(country=None, limit=5):
    """Test searching companies"""
    print("\n" + "="*60)
    print(f"Testing Search Companies (country={country}, limit={limit})")
    print("="*60)

    params = {"limit": limit}
    if country:
        params["country"] = country

    response = requests.get(f"{BASE_URL}/companies/search", params=params)
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"\nFound {data['count']} companies:")
        for i, company in enumerate(data['data'], 1):
            print(f"\n  {i}. {company.get('name')}")
            print(f"     Country: {company.get('country')}")
            print(f"     Website: {company.get('website')}")
        return True
    else:
        print(f"Response: {json.dumps(response.json(), indent=2)}")

    return False

def test_get_statistics():
    """Test getting statistics"""
    print("\n" + "="*60)
    print("Testing Get Statistics")
    print("="*60)

    response = requests.get(f"{BASE_URL}/stats")
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"\nTotal Companies: {data.get('total_companies'):,}")

        print("\nTop 5 Countries:")
        for country in data.get('top_countries', [])[:5]:
            print(f"  {country['country']:<20} {country['count']:>10,}")

        print("\nCompany Sizes:")
        for size in data.get('company_sizes', []):
            print(f"  {size['size']:<20} {size['count']:>10,}")

        return True
    else:
        print(f"Response: {json.dumps(response.json(), indent=2)}")

    return False

def main():
    print("\n" + "="*60)
    print("European Companies API - Test Suite")
    print("="*60)
    print(f"Base URL: {BASE_URL}")

    results = []

    # Test health
    results.append(("Health Check", test_health()))

    # Test statistics
    results.append(("Statistics", test_get_statistics()))

    # Test search by country
    results.append(("Search (Germany)", test_search_companies("germany", 5)))
    results.append(("Search (France)", test_search_companies("france", 3)))

    # Test domain lookup (you can customize these domains based on your data)
    results.append(("Domain Lookup", test_get_company_by_domain("google.de")))

    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name:<30} {status}")

    total = len(results)
    passed = sum(1 for _, p in results if p)
    print(f"\nTotal: {passed}/{total} tests passed")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API")
        print("Make sure the API is running: uvicorn main:app --reload")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
