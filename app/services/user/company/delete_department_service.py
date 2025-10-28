# app/services/company_service.py
from fastapi import HTTPException, status
from bson import ObjectId
from app.core.databse import db
async def delete_department_service( company_id: str, filtered_dept: list):

    company = await db["users"].find_one({"_id": ObjectId(company_id), "role": "company"})
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    result = await db["users"].update_one(
        {"_id": ObjectId(company_id)},
        {"$set": {"department": filtered_dept}}
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update department"
        )

    return {"message": "Department deleted successfully"}
