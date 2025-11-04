# app/core/save_embedding.py
from app.core.databse import db


async def delete_embedding_by_id(user_id: str, company_id: str) -> bool:

    collection = db["embeddings"]
    result = await collection.delete_one({"emp_id": user_id, "company_id": company_id})
    return result.deleted_count > 0
