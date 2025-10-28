# API Authentication Guide

The European Companies API uses **Bearer Token Authentication** to secure access to the endpoints.

## 🔑 Your API Access Token

```
pdl_sk_live_a8f3d9e2b1c4f7a6e5d8c2b9f4a1e7d3
```

**Important:** Keep this token secret and never commit it to version control!

---

## 📝 How to Use the Token

### cURL Examples

#### Get company by domain:
```bash
curl -H "Authorization: Bearer pdl_sk_live_a8f3d9e2b1c4f7a6e5d8c2b9f4a1e7d3" \
  "https://fetch-companies-data-production.up.railway.app/company/domain/example.com"
```

#### Search companies:
```bash
curl -H "Authorization: Bearer pdl_sk_live_a8f3d9e2b1c4f7a6e5d8c2b9f4a1e7d3" \
  "https://fetch-companies-data-production.up.railway.app/companies/search?country=germany&limit=10"
```

#### Get statistics:
```bash
curl -H "Authorization: Bearer pdl_sk_live_a8f3d9e2b1c4f7a6e5d8c2b9f4a1e7d3" \
  "https://fetch-companies-data-production.up.railway.app/stats"
```

---

### Python Example

```python
import requests

# Your API token
API_TOKEN = "pdl_sk_live_a8f3d9e2b1c4f7a6e5d8c2b9f4a1e7d3"
BASE_URL = "https://fetch-companies-data-production.up.railway.app"

# Set up headers
headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

# Get company by domain
response = requests.get(
    f"{BASE_URL}/company/domain/example.com",
    headers=headers
)
print(response.json())

# Search companies
response = requests.get(
    f"{BASE_URL}/companies/search",
    headers=headers,
    params={"country": "germany", "limit": 10}
)
print(response.json())
```

---

### JavaScript/Node.js Example

```javascript
const API_TOKEN = 'pdl_sk_live_a8f3d9e2b1c4f7a6e5d8c2b9f4a1e7d3';
const BASE_URL = 'https://fetch-companies-data-production.up.railway.app';

// Using fetch
async function getCompanyByDomain(domain) {
  const response = await fetch(`${BASE_URL}/company/domain/${domain}`, {
    headers: {
      'Authorization': `Bearer ${API_TOKEN}`
    }
  });
  return await response.json();
}

// Using axios
const axios = require('axios');

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Authorization': `Bearer ${API_TOKEN}`
  }
});

// Get company
api.get('/company/domain/example.com')
  .then(response => console.log(response.data));

// Search companies
api.get('/companies/search', {
  params: { country: 'germany', limit: 10 }
})
  .then(response => console.log(response.data));
```

---

### PHP Example

```php
<?php
$api_token = 'pdl_sk_live_a8f3d9e2b1c4f7a6e5d8c2b9f4a1e7d3';
$base_url = 'https://fetch-companies-data-production.up.railway.app';

// Set up headers
$headers = [
    'Authorization: Bearer ' . $api_token
];

// Get company by domain
$ch = curl_init($base_url . '/company/domain/example.com');
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$response = curl_exec($ch);
curl_close($ch);

$data = json_decode($response, true);
print_r($data);
?>
```

---

## 🚫 Unauthenticated Requests

### Public Endpoints (No token required):
- `GET /` - Root endpoint
- `GET /health` - Health check

### Protected Endpoints (Token required):
- `GET /company/domain/{domain}` - Get company by domain
- `GET /companies/search` - Search companies
- `GET /stats` - Get statistics

---

## ⚠️ Error Responses

### Missing Token:
```json
{
  "detail": "Not authenticated"
}
```
Status Code: `403 Forbidden`

### Invalid Token:
```json
{
  "detail": "Invalid or missing authentication token"
}
```
Status Code: `401 Unauthorized`

---

## 🔒 Security Best Practices

1. **Never commit your token to git**
   - Keep it in `.env` file (already in `.gitignore`)
   - Use environment variables in production

2. **Use HTTPS only**
   - Always use `https://` URLs
   - Never send tokens over HTTP

3. **Rotate tokens regularly**
   - Change your token periodically
   - Update the `API_ACCESS_TOKEN` in `.env`

4. **Don't share tokens**
   - Keep your token private
   - Use separate tokens for different applications if needed

---

## 🔄 Rotating Your Token

To generate a new token:

```python
import secrets
new_token = f"pdl_sk_live_{secrets.token_hex(16)}"
print(new_token)
```

Then update:
1. `.env` file: `API_ACCESS_TOKEN=new_token_here`
2. Redeploy your API
3. Update all client applications

---

## 📊 Testing with Swagger UI

Visit: https://fetch-companies-data-production.up.railway.app/docs

1. Click the "Authorize" button (🔓)
2. Enter your token: `pdl_sk_live_a8f3d9e2b1c4f7a6e5d8c2b9f4a1e7d3`
3. Click "Authorize"
4. Now you can test all endpoints interactively!

---

## 📞 Support

If you have issues with authentication, check:
1. Token is included in the `Authorization` header
2. Header format is exactly: `Authorization: Bearer YOUR_TOKEN`
3. No extra spaces or characters in the token
4. Using the latest token from your `.env` file
