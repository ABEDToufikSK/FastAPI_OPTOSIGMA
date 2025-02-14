from fastapi import FastAPI
import requests
import time
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

# Initialize FastAPI
app = FastAPI()

# Akeneo API configuration
AKENEO_API_URL = "http://51.91.120.17"
CLIENT_ID = "FastAPI"
SECRET = "*?;$&MygGH8!X8v"

# OpenAI configuration
chat_model = ChatOpenAI(openai_api_key="sk-...")  # Replace with your valid OpenAI API key

# Global variable to store the token and its expiry time
access_token = None
token_expiry = 0

# Function to get OAuth2 access token
def get_access_token():
    global access_token, token_expiry
    
    # Check if the token is still valid
    if access_token and time.time() < token_expiry:
        return access_token
    
    # Request a new token
    token_url = f"{AKENEO_API_URL}/api/oauth/v1/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": SECRET,
        "grant_type": "password",  # Use the correct grant type
        "username": "FastAPI",  # Replace with actual username
        "password": "*?;$&MygGH8!X8v"   # Replace with actual password
    }
    response = requests.post(token_url, data=payload)
    
    # Debugging: Print the full response
    print("Token endpoint response:", response.status_code, response.text)
    
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get("access_token")
        token_expiry = time.time() + token_data.get("expires_in", 3600)  # Default to 1 hour
        return access_token
    else:
        raise Exception(f"Failed to get access token: {response.status_code}, {response.text}")

# Chat request model
class ChatRequest(BaseModel):
    query: str

# Chat endpoint
@app.post("/chat")
def chat_with_ai(request: ChatRequest):
    try:
        # Get access token
        access_token = get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}

        # Fetch products from Akeneo
        response = requests.get(f"{AKENEO_API_URL}/api/rest/v1/products", headers=headers)
        
        # Debugging: Print the full response
        print("Products endpoint response:", response.status_code, response.text)
        
        if response.status_code != 200:
            return {"error": f"Failed to fetch products from Akeneo: {response.status_code}, {response.text}"}
        
        products = response.json()

        # Build a question for ChatGPT
        product_list = ", ".join([p["identifier"] for p in products.get("_embedded", {}).get("items", [])])
        user_message = f"L'utilisateur cherche un produit correspondant à : {request.query}. Voici nos produits : {product_list}"

        # Query ChatGPT via Langchain
        ai_response = chat_model([HumanMessage(content=user_message)])
        response_content = ai_response.content if ai_response else "No response from AI"

        return {"response": response_content}

    except requests.exceptions.RequestException as e:
        return {"error": f"HTTP request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)