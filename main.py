from fastapi import FastAPI
import requests
from pydantic import BaseModel
#from langchain_community.chat_models import ChatOpenAI  # Mise à jour de l'import
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

# Initialisation de FastAPI
app = FastAPI()

# Configuration API Akeneo
AKENEO_API_URL = "http://51.91.120.17"
CLIENT_ID = "1_4tarkxrl2lus0ogs400ocs4wgwsk88gokwoksosg80o44wck4g"
SECRET = "3im552it5vcwkow844owc004g8kggk8w0g0kko4ow048o0kwgw"

# # Configuration API Akeneo
# AKENEO_API_URL = "http://51.91.120.17"
# CLIENT_ID = "FastAPI"
# SECRET = "*?;$&MygGH8!X8v"



# Classe pour gérer les requêtes du chatbot
class ChatRequest(BaseModel):
    query: str

# Initialisation de ChatOpenAI depuis langchain_community (clé OpenAI à fournir)
chat_model = ChatOpenAI(openai_api_key="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")

# Route pour interroger Akeneo et ChatGPT
@app.post("/chat")
def chat_with_ai(request: ChatRequest):
    try:
        # Appeler Akeneo pour récupérer des produits
        response = requests.get(f"{AKENEO_API_URL}/api/rest/v1/products", auth=(CLIENT_ID, SECRET))
        
        if response.status_code != 200:
            return {"error": "Failed to fetch products from Akeneo"}
        
        products = response.json()

        # Construire une question pour ChatGPT en fonction des produits Akeneo
        product_list = ", ".join([p["identifier"] for p in products.get("_embedded", {}).get("items", [])])
        user_message = f"L'utilisateur cherche un produit correspondant à : {request.query}. Voici nos produits : {product_list}"

        # Interroger ChatGPT via Langchain
        ai_response = chat_model([HumanMessage(content=user_message)])
        response_content = ai_response.content if ai_response else "No response from AI"

        return {"response": response_content}

    except Exception as e:
        return {"error": str(e)}

# Point d'entrée pour exécuter l'application si nécessaire
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)