from fastapi import APIRouter, HTTPException, Response, Depends, Body, status, BackgroundTasks, Query
from app.models.userModel import UserCreate, AddDepartmentModel, SubDepartmentUpdate
from bson import ObjectId
from app.services.user.user_service import create_user
from app.models.signInModel import SignInModel
from app.services.user.sign_in_service import sign_in_user
from app.services.user.sign_out_service import sign_out_user
from app.services.user.get_all_company import get_all_companies_by_parent, get_single_company
from app.utils.role_guard import get_current_user
from app.utils.role_guard import require_role
from app.services.user.get_all_employee_by_companyId import get_all_employee_by_company_id
from app.core.databse import db
from app.services.user.get_single_user_service import get_user_by_id
from app.services.user.company.delete_department_service import delete_department_service
from app.services.user.company.delete_subdepartment_service import delete_subdepartment_service
from app.auth.email_token import send_verification_email ,confirm_verification_token
router = APIRouter(tags=["auth"])


@router.post("/signup")  # group signup
async def add_user(user: UserCreate,background_tasks: BackgroundTasks):
    try:
        data = user.model_dump()
        collection = db["users"]
        existing_user = await collection.find_one({"email": data["email"]})
        if existing_user:
           if existing_user["is_verified"]:
             raise HTTPException(
                 status_code=status.HTTP_400_BAD_REQUEST,
                 detail="Email already registered"
              )
           else:
              await send_verification_email(background_tasks,data["email"])
              return{"message": "Email Already Exist but not verified. Verification email sent!"}
        user_id = await create_user(data)
        await send_verification_email(background_tasks, data["email"])
        return {"message": "Signup Successful,Please verify your email!", "id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/verify-email")
async def verify_email(token: str = Query(...)):
    try:
        email = confirm_verification_token(token)
        collection = db["users"]
        user = await collection.find_one({"email": email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user["is_verified"]:
            return {"message": "Email already verified!"}

        await collection.update_one(
            {"email": email},
            {"$set": {"is_verified": True}}
        )
        return {"message": "Email verification successful!"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/signin")
async def sign_in(data: SignInModel, response: Response):
    try:
        # Step 1: Find the user by email
        user = await db["users"].find_one({"email": data.email})

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Step 2: Check email verification
        if not user.get("is_verified", False):
            raise HTTPException(
                status_code=403,
                detail="Please verify your email before logging in."
            )

        # Step 3: Call your existing login logic
        result = await sign_in_user(data.model_dump(), response)
        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sign_out")
async def sign_out(response: Response):
    return await sign_out_user(response)


# Route to add a new department

@router.patch("/company/add-department")
async def add_department(data: AddDepartmentModel):
    try:
        result = await db.users.update_one(
            {"_id": ObjectId(data.id)},
            {
                "$addToSet": {"department": data.department},  # or "$each": data.department if list
                "$currentDate": {"updatedAt": True}
            }
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="User not found or department already exists")

        return {"message": "department added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/company/add-subdepartment")
async def add_subdepartment(data: SubDepartmentUpdate):
    try:
        result = await db.users.update_one(
            {"_id": ObjectId(data.id)},
            {
                "$addToSet": {"subdepartment": data.subdepartment},
                "$currentDate": {"updatedAt": True}
            }
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="User not found or subdepartment already exists")

        return {"message": "Subdepartment added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/company/delete-department")
async def delete_department(payload: dict):
    data = payload.get("payload")
    if not data:
        return {"error": "Invalid request structure. Expected { payload: {...} }"}

    company_id = data["id"]
    filtered_dept = data["filteredDept"]

    return await delete_department_service(company_id, filtered_dept)


@router.patch("/company/delete-subdepartment")
async def delete_subdepartment(payload: dict):
    data = payload.get("payload")
    if not data:
        return {"error": "Invalid request structure. Expected { payload: {...} }"}

    company_id = data["id"]
    filtered_subdept = data["filteredSubDept"]

    return await delete_subdepartment_service(company_id, filtered_subdept)


@router.get("/all-company")
async def get_all_company(user=Depends(require_role(["group", "company"]))):
    try:
        parent_id = user["user_id"]
        print("parent_id>>", parent_id)
        companies = []
        if user["role"] == "group":
            companies = await get_all_companies_by_parent(parent_id)
        if user["role"] == "company":
            companies = await get_single_company(parent_id)
        print("companies>>", companies)
        return companies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/all-employee")
async def get_all_employee(
        data: dict = Body(...),
):
    try:
        company_id = data.get("company_id")
        if not company_id:
            raise HTTPException(status_code=400, detail="company_id is required")
        companies = await get_all_employee_by_company_id(company_id)
        return companies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return await get_user_by_id(current_user["user_id"])


@router.get("/single-user")
async def get_single_user(user_id: str):
    user = await get_user_by_id(user_id)
    return user
