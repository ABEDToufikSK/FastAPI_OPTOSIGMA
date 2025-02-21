from fastapi import FastAPI
import redis
import json
import requests
import time
import os
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
import threading

# Initialize FastAPI
app = FastAPI()

# 🔹 Redis Configuration
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
CACHE_EXPIRY_TIME = 604800  # 7 days

# 🔹 Initialize Redis Client with Error Handling
try:
    redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
    redis_client.ping()  # Test connection
    print("🟢 Redis connection successful")
except Exception as e:
    print(f"🔴 Redis connection failed: {e}")
    redis_client = None  # Prevent further Redis calls if connection failed

# 🔹 OpenAI Configuration
OPENAI_API_KEY = "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"
if not OPENAI_API_KEY:
    raise ValueError("🔴 Missing OpenAI API Key! Set 'OPENAI_API_KEY' as an environment variable.")

chat_model = ChatOpenAI(openai_api_key=OPENAI_API_KEY)

# ------------------------------
# 1️⃣ 🛑 Retrieve Product Data from Redis
# ------------------------------
def get_cached_products():
    """Retrieve cached products from Redis"""
    if not redis_client:
        return {"error": "Redis is not available"}
    
    cached_data = redis_client.get("akeneo_products")
    if cached_data:
        print("🟢 Using cached product data from Redis")
        return json.loads(cached_data)
    
    print("🔴 No cached product data found in Redis")
    return {"error": "No products available"}

# ------------------------------
# 2️⃣ 🔵 OpenAI Response Caching
# ------------------------------
def get_cached_chat_response(query):
    """Retrieve cached chat response from Redis"""
    if not redis_client:
        return None
    return redis_client.get(f"chat_response:{query}")

def store_chat_response(query, response):
    """Store chat response in Redis for 7 days"""
    if redis_client:
        redis_client.setex(f"chat_response:{query}", CACHE_EXPIRY_TIME, response)

# ------------------------------
# 3️⃣ 🔥 Detect Product-Related Queries
# ------------------------------
PRODUCT_KEYWORDS = ["product", "catalog", "price", "specifications", "availability", "model", "features"]

def is_product_query(user_query):
    """Check if the user's query is product-related"""
    user_query_lower = user_query.lower()
    return any(keyword in user_query_lower for keyword in PRODUCT_KEYWORDS)

# ------------------------------
# 4️⃣ 🔥 FastAPI Chat Endpoint (Uses Caching & Logic)
# ------------------------------
class ChatRequest(BaseModel):
    query: str

@app.post("/chat")
def chat_with_ai(request: ChatRequest):
    try:
        user_query = request.query

        # 🔹 Step 1: Check if response is already cached
        cached_response = get_cached_chat_response(user_query)
        if cached_response:
            print("🟢 Returning cached AI response from Redis")
            return {"response": cached_response}

        # 🔹 Step 2: Determine if the query is about a product
        if is_product_query(user_query):
            print("🔵 Detected product-related query. Fetching from Redis...")
            products = get_cached_products()
            
            if "error" in products:
                return products

            # 🔹 Step 3: Create a message for OpenAI with product data
            product_list = ", ".join(products.values())
            user_message = f"L'utilisateur cherche un produit correspondant à : {user_query}. Voici nos produits : {product_list}"

        else:
            print("🟢 General query detected. Letting ChatGPT reply freely.")
            user_message = user_query  # Let ChatGPT generate a free response

        # 🔹 Step 4: Query OpenAI (Either with product data or general question)
        ai_response = chat_model.invoke([HumanMessage(content=user_message)])  # FIXED: Correct invocation
        response_content = ai_response.content if ai_response else "No response from AI"

        # 🔹 Step 5: Store the response in Redis
        store_chat_response(user_query, response_content)

        return {"response": response_content}

    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

# ------------------------------
# 5️⃣ 🔄 Auto-Refresh Redis Cache Every 7 Days
# ------------------------------
def auto_refresh_cache():
    """Background thread that refreshes Redis cache every 7 days."""
    while True:
        time.sleep(CACHE_EXPIRY_TIME)  # Wait 7 days
        print("🔄 Refreshing product cache in Redis...")
        
        # Simulating refresh (in reality, you'd fetch new data from Akeneo)
        fake_products = {"product_001": "Sample Product 1", "product_002": "Sample Product 2"}
        redis_client.set("akeneo_products", json.dumps(fake_products), ex=CACHE_EXPIRY_TIME)
        
        print(f"🟢 Redis cache updated with {len(fake_products)} products!")

# Run Background Thread
cache_thread = threading.Thread(target=auto_refresh_cache, daemon=True)
cache_thread.start()

# ------------------------------
# 6️⃣ 🚀 Run FastAPI Server
# ------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
