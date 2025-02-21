import redis
import json

# Redis Configuration
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

# Connect to Redis with Exception Handling
try:
    redis_client = redis.StrictRedis(
        host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True
    )
    redis_client.ping()  # Test connection
except redis.ConnectionError:
    print("❌ Redis connection failed! Make sure Redis is running.")
    exit(1)

# Retrieve Data from Redis
def get_cached_products():
    try:
        cached_data = redis_client.get("akeneo_products")
        if cached_data:
            products = json.loads(cached_data)
            return products
        else:
            return {"error": "No product data found in Redis"}
    except redis.RedisError as e:
        return {"error": f"Redis error: {str(e)}"}

if __name__ == "__main__":
    products = get_cached_products()

    if "error" in products:
        print(products["error"])
    else:
        print(f"🟢 Retrieved {len(products)} products from Redis:")
        
        # Print only the first 10 products (prevent excessive output)
        for idx, (identifier, name) in enumerate(products.items()):
            print(f"{identifier}: {name}")
            if idx == 9:  # Limit output to 10 products
                print("... (Showing only first 10 products)")
                break
