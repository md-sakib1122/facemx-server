from bson import ObjectId
from app.core.databse import db


async def get_all_employee_by_company_id(company_id: str):

    collection = db["users"]
    cursor = collection.find({"company_id": company_id,"role":"employee"},)

    # Convert ObjectId fields to string
    employees = []
    async for doc in cursor:
        # Convert ObjectId to str and remove password from output
        employees.append({
            "id": str(doc["_id"]),
            "name": doc.get("name"),
            "email":doc.get("email"),
            "role": doc.get("role"),
            "company_id": doc.get("company_id"),
            "emp_id": doc.get("emp_id"),
            "group_id": doc.get("group_id"),
            "userDept": doc.get("userDept"),
            "locations": doc.get("locations"),
            "userSubDept": doc.get("userSubDept"),
        })

    return employees
