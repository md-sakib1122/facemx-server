from app.core.databse import db
from bson import ObjectId
from fastapi import HTTPException, status

async def get_all_companies_by_parent(parent_id: str):

    try:
        collection = db["users"]
        cursor = collection.find({"parent": parent_id})
        companies = []
        async for doc in cursor:
            # Convert ObjectId to str and remove password from output
            companies.append({
                "id": str(doc["_id"]),
                "name": doc.get("name"),
                "email": doc.get("email"),
                "company_code": doc.get("company_code"),
                "address": doc.get("address"),
                "city": doc.get("city"),
                "fax": doc.get("fax"),
                "phone": doc.get("phone"),
                "tax_no": doc.get("tax_no"),
                "country": doc.get("country"),
                "abbreviate_name":doc.get("abbreviate_name"),
                "role": doc.get("role"),
                "parent": doc.get("parent"),
                "department": doc.get("department", []),
                "subdepartment": doc.get("subdepartment", []),
                "createdAt": doc.get("createdAt"),
                "updatedAt": doc.get("updatedAt"),
            })
        return companies
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))




async def get_single_company(company_id: str):
    try:
        collection = db["users"]
        cursor = collection.find({"_id": ObjectId(company_id)})
        companies = []
        async for doc in cursor:
            # Convert ObjectId to str and remove password from output
            companies.append({
                "id": str(doc["_id"]),
                "name": doc.get("name"),
                "email": doc.get("email"),
                "role": doc.get("role"),
                "parent": doc.get("parent"),
                "department": doc.get("department", []),
                "subdepartment": doc.get("subdepartment", []),
                "createdAt": doc.get("createdAt"),
                "updatedAt": doc.get("updatedAt"),
            })
        return companies
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
