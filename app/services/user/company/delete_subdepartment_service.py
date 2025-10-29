# app/services/company_service.py
from fastapi import HTTPException, status
from bson import ObjectId
from app.core.databse import db
async def delete_subdepartment_service( company_id: str, filtered_subdept: list):

    company = await db["users"].find_one({"_id": ObjectId(company_id), "role": "company"})
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    result = await db["users"].update_one(
        {"_id": ObjectId(company_id)},
        {"$set": {"subdepartment": filtered_subdept}}
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update subdepartment"
        )

    return {"message": "Subdepartment deleted successfully"}
