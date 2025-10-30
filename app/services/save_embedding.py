# import json
# import os
#
# EMBEDDINGS_FILE = "data/face_embeddings.json"
# os.makedirs("data", exist_ok=True)
#
# async def save_embedding(embedding: list[float], image_path: str, name: str,notes: str):
#     # Load existing data if file exists
#     data = []
#     if os.path.exists(EMBEDDINGS_FILE):
#         with open(EMBEDDINGS_FILE, "r") as f:
#             data = json.load(f)
#
#     # Append new entry
#     data.append({
#         "embedding": embedding,
#         "image_path": image_path,
#         "id": name,
#         "notes": notes
#     })
#
#     # Save back to file
#     with open(EMBEDDINGS_FILE, "w") as f:
#         json.dump(data, f, indent=4)

# app/core/save_embedding.py
from app.core.databse import db

async def save_embedding(embedding: list[float], image_path: str, emp_id: str, notes: str , company_id: str):
    collection = db["embeddings"]   # 👈 collection name
    document = {
        "embedding": embedding,
        "image_path": image_path,
        "emp_id": emp_id,
        "notes": notes,
        "company_id": company_id,
    }
    result = await collection.insert_one(document)
    return str(result.inserted_id)

