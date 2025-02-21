import redis
import requests
import json
import time

# Redis Configuration
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
CACHE_EXPIRY_TIME = 604800  # 7 days

redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

# Akeneo API Configuration
AKENEO_API_URL = "http://51.91.120.17"
CLIENT_ID = "1_4tarkxrl2lus0ogs400ocs4wgwsk88gokwoksosg80o44wck4g"
CLIENT_SECRET = "3im552it5vcwkow844owc004g8kggk8w0g0kko4ow048o0kwgw"
USERNAME = "FastAPI"
PASSWORD = "*?;$&MygGH8!X8v"

# Akeneo Authentication to Get Akeneo Access Token
def get_access_token():
    token_url = f"{AKENEO_API_URL}/api/oauth/v1/token"
    payload = {
        "grant_type": "password",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "username": USERNAME,
        "password": PASSWORD
    }
    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f"❌ Failed to get access token: {response.status_code}, {response.text}")
        return None

# Function to Get Total Product Count from Akeneo
def get_total_product_count(access_token):
    url = f"{AKENEO_API_URL}/api/rest/v1/products?limit=1&with_count=true"  # Enable count
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers)
    print(f"🔍 Total count request status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"🔍 API Response: {json.dumps(data, indent=2)}")  # Debugging output
        return data.get("items_count", 0)
    else:
        print(f"❌ Failed to fetch total product count: {response.status_code}, {response.text}")
        return 0

# Function to Fetch Products and Store in Redis using "search_after" pagination with progress %
def fetch_and_store_products():
    access_token = get_access_token()
    if not access_token:
        return {"error": "Failed to authenticate with Akeneo"}

    # Get total product count
    total_products = get_total_product_count(access_token)
    if total_products == 0:
        print("❌ Could not retrieve total product count. Fetching may not show accurate progress.")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{AKENEO_API_URL}/api/rest/v1/products?limit=50"

    all_products = {}
    next_page_cursor = None
    total_fetched = 0  # Counter for total products fetched

    print(f"🔄 Fetching {total_products} products from Akeneo...")

    while total_fetched < total_products:  # Stop fetching when total is reached
        if next_page_cursor:
            url = f"{AKENEO_API_URL}/api/rest/v1/products?limit=50&search_after={next_page_cursor}"
        else:
            url = f"{AKENEO_API_URL}/api/rest/v1/products?limit=50"

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            products = data.get("_embedded", {}).get("items", [])

            if not products:  # If no products are returned, stop fetching
                print("🚨 No more products to fetch. Stopping.")
                break

            for p in products:
                identifier = p["identifier"]
                name = p.get("values", {}).get("name", [{"data": "Unnamed Product"}])[0]["data"]
                all_products[identifier] = name

            # Update count and progress
            total_fetched += len(products)
            progress_percentage = (total_fetched / total_products) * 100 if total_products else 0
            print(f"✅ Fetching products... {progress_percentage:.2f}% complete ({total_fetched}/{total_products})")

            # **Fix next_page_cursor**
            next_page_cursor = data["_embedded"]["items"][-1]["identifier"] if products else None

            if not next_page_cursor:
                print("🛑 No more pages available in API. Stopping.")
                break
        else:
            print(f"❌ API Error: {response.status_code}, {response.text}")
            break


    # Store in Redis as a JSON object
    redis_client.set("akeneo_products", json.dumps(all_products), ex=CACHE_EXPIRY_TIME)
    print(f"🎉 Fetch complete! 100% of products retrieved ({total_fetched}/{total_products}).")
    print(f"🟢 Redis database updated with {total_fetched} products.")

    return all_products

# Run the function to fetch and store products in Redis
if __name__ == "__main__":
    fetch_and_store_products()
