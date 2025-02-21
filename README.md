## 📌 **README - Chatbot IA pour Magento 2 avec FastAPI et Redis**

### 🛠 **Présentation du Projet**
#### 📍 Contexte
OptoSigma est un site e-commerce spécialisé dans la vente de composants **photonique et optique**, disposant d’un catalogue de **15 000+ produits**. Trouver le bon produit et vérifier sa compatibilité avec d’autres composants est un **défi majeur** pour les clients.

#### 🎯 Objectif
Développer un **chatbot intelligent** pour **Magento 2**, intégrant **ChatGPT** et **Akeneo API**, afin de :
- **Recommander des produits** en fonction des besoins des clients.
- **Vérifier la compatibilité** des composants et proposer des **bundles**.
- **Assurer une expérience fluide** grâce à une IA avancée.
- **Ne suggérer que des produits disponibles** sur le site.

---

## 🔧 **Architecture et Technologies**
### 🏗 **Architecture Générale**
- **Frontend** : React.js / Vue.js *(interface utilisateur)*
- **Backend** : Magento 2 (PHP) + FastAPI (Python) *(gestion IA)*
- **Base de Données** : PostgreSQL / Redis *(cache produits)*
- **API Utilisées** :
  - **Akeneo API** *(gestion des produits)*
  - **OpenAI API** *(ChatGPT pour l’IA conversationnelle)*
  - **Magento API** *(gestion panier & utilisateurs)*

### ⚙ **Technologies**
- **Magento 2.4.7** *(E-commerce)*
- **FastAPI** *(Backend IA)*
- **LangChain** *(Optimisation des requêtes IA)*
- **Redis** *(Stockage cache produits)*
- **OpenAI API** *(ChatGPT 4 pour les recommandations)*

---

## 📌 **Fonctionnalités Principales**
✅ **Interface conversationnelle** intégrée à Magento 2  
✅ **Recherche intelligente** et recommandations personnalisées  
✅ **Proposition de bundles compatibles**  
✅ **Accès en temps réel** aux données produits via Akeneo API  
✅ **Mémorisation du contexte** de conversation  
✅ **Ajout des produits recommandés au panier**  

---

## 🏗 **Installation et Configuration**
### **1️⃣ Cloner le projet**
```sh
git clone https://github.com/your-repo/fastapi-chatbot.git
cd fastapi-chatbot
```

### **2️⃣ Créer et activer un environnement virtuel**
```sh
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate      # Windows
```

### **3️⃣ Installer les dépendances**
```sh
pip install -r requirements.txt
```

### **4️⃣ Configurer les variables d’environnement**
Créer un fichier **`.env`** :
```env
OPENAI_API_KEY=sk-proj-XXXXXXXXXXXXX
REDIS_HOST=localhost
REDIS_PORT=6379
AKENEO_API_URL=http://51.91.120.17
AKENEO_CLIENT_ID=your_client_id
AKENEO_CLIENT_SECRET=your_client_secret
AKENEO_USERNAME=FastAPI
AKENEO_PASSWORD=your_password
```

### **5️⃣ Lancer le serveur FastAPI**
```sh
uvicorn main:app --reload
```
📍 Accédez à la documentation API interactive : **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

## 🔥 **Endpoints API**
| Méthode | Endpoint | Description |
|---------|---------|-------------|
| **POST** | `/chat` | Envoie une requête à ChatGPT en utilisant les produits stockés en cache |
| **GET** | `/products` | Récupère les produits depuis Redis (sans requête Akeneo) |
| **GET** | `/health` | Vérifie si le serveur est en ligne |

---

## 📦 **Déploiement**
### **Docker (Optionnel)**
Si vous souhaitez utiliser Docker pour exécuter l'API :
```sh
docker build -t chatbot-api .
docker run -p 8000:8000 --env-file .env chatbot-api
```

---

## 📅 **Planning**
### **Phase 1 : Mise en place des bases**
- Installation de Magento 2 et du module chatbot
- Création de l’interface utilisateur React.js / Vue.js

### **Phase 2 : Connexion à l’IA**
- Développement du backend **FastAPI**
- Intégration de **ChatGPT via LangChain**
- Tests des interactions et compréhension utilisateur

### **Phase 3 : Connexion à Akeneo**
- Récupération des produits via **Akeneo API**
- Stockage et gestion des données produits via **Redis**
- Implémentation des **règles de compatibilité**

### **Phase 4 : Intégration finale et tests**
- Intégration complète **Magento - IA - Akeneo**
- **Tests UX et fonctionnels**
- Mise en production et monitoring

---

## 🔍 **Suivi & Maintenance**
✅ **Mise en cache des réponses ChatGPT** pour éviter la surconsommation de l’API  
✅ **Surveillance des logs et monitoring des performances**  
✅ **Mises à jour IA et ajustements UX**  

---

📌 **Dernière mise à jour :** `Février 2025`  
✉ **Contact :** `t.abed@optosigma-europe.com` 🚀
