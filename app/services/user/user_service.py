from datetime import datetime
from app.core.databse import db
from fastapi import HTTPException, status
from app.auth.password_utils import hash_password

async def create_user(data: dict):
    collection = db["users"]
    hashed_pw = hash_password(data["password"])
    print("create user data",data)
    # check if email already exists
    existing_user = await collection.find_one({"email": data["email"]})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    document = {}

    if data["role"] in ["group", "company"]:
        document = {
            "name": data["name"],
            "email": data["email"],
            "password": hashed_pw,
            "role": data["role"],
            #company
            "parent": data.get("parent"),
            "department": [],
            "subdepartment": [],
            "company_code": data.get("company_code"),
            "address": data.get("address"),
            "city": data.get("city"),
            "fax":data.get("fax"),
            "phone": data.get("phone"),
            "tax_no": data.get("tax_no"),
            "country": data.get("country"),
            "abbreviate_name": data.get("abbreviate_name"),
            #company
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow(),
        }

    elif data["role"] == "employee":
        document = {
            "name": data["name"],
            "email": data["email"],
            "password": hashed_pw,
            "role": data["role"],
            "company_id": data.get("company_id"),
            "emp_id": data.get("emp_id"),
            "group_id": data.get("group_id"),
            "userSubDept" :data.get("userSubDept"),
            "userDept":data.get("userDept"),
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow(),
        }

    collection.insert_one(document)
    result = await collection.insert_one(document)

    return str(result.inserted_id)
