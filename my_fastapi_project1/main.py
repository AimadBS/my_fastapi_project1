from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson import ObjectId
import json
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["my_database"]  # Base de données
collection = db["my_collection"]  # Collection

# Configurer CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autoriser toutes les origines (modifiable)
    allow_credentials=True,
    allow_methods=["*"],  # Autoriser toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Autoriser tous les headers
)

# Routes API

@app.get("/")
def home():
    """Message de bienvenue pour tester la connexion."""
    return {"message": "Bienvenue sur l'API FastAPI avec MongoDB!"}


@app.get("/items")
def get_items():
    """Récupérer tous les éléments depuis MongoDB."""
    items = list(collection.find())  # On récupère tous les documents
    for item in items:
        item["_id"] = str(item["_id"])  # Conversion ObjectId -> string
    return items

class Item(BaseModel):
    message: str

@app.post("/items")
def create_item(item: Item):
    new_item = {"message": item.message}
    result = collection.insert_one(new_item)
    return {"id": str(result.inserted_id), "message": item.message}


@app.delete("/items/{item_id}")
def delete_item(item_id: str):
    """Supprimer un élément par son ID."""
    result = collection.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Élément introuvable")
    return {"message": "Élément supprimé avec succès"}
