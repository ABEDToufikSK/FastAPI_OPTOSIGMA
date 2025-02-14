import requests

# Step 1: Obtain an access token
token_url = "http://51.91.120.17/api/oauth/v1/token"
client_id = "1_4tarkxrl2lus0ogs400ocs4wgwsk88gokwoksosg80o44wck4g"
secret = "3im552it5vcwkow844owc004g8kggk8w0g0kko4ow048o0kwgw"

payload = {
        "client_id": "FastAPI",
        "client_secret": "*?;$&MygGH8!X8v",
        "grant_type": "users"
    }

token_response = requests.post(token_url, data=payload)
token_data = token_response.json()

if "access_token" in token_data:
    access_token = token_data["access_token"]

    # Step 2: Use the access token to make the API request
    url = "http://51.91.120.17/api/rest/v1/products"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)
    print(response.status_code)
    print(response.json())
else:
    print("Failed to obtain access token:", token_data)