from fastapi import APIRouter, HTTPException, Response,Depends,Body
from app.models.userModel import UserCreate , AddDepartmentModel , SubDepartmentUpdate
from bson import ObjectId
from app.services.user.user_service import create_user
from app.models.signInModel import SignInModel
from app.services.user.sign_in_service import sign_in_user
from app.services.user.sign_out_service import sign_out_user
from app.services.user.get_all_company import get_all_companies_by_parent,get_single_company
from app.utils.role_guard import get_current_user
from app.utils.role_guard import require_role
from app.services.user.get_all_employee_by_companyId import get_all_employee_by_company_id
from app.core.databse import db
from app.services.user.get_single_user_service import get_user_by_id
from app.services.user.company.delete_department_service import delete_department_service
from app.services.user.company.delete_subdepartment_service import delete_subdepartment_service
router = APIRouter(tags=["auth"])

@router.post("/signup")  # group signup
async def add_group(user: UserCreate):
    try:
        user_id = await create_user(user.model_dump())
        return {"message": "group created successfully", "id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/signin")
async def sign_in(data: SignInModel, response: Response):
    print("hit korche",data)
    try:
        result = await sign_in_user(data.model_dump(),response)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sign_out")
async def sign_out(response: Response):
    return await sign_out_user(response)

@router.post("/create-company")  # company signup
async def add_company(company: UserCreate):
    try:
        print("company->>", company)
        company_id = await create_user(company.model_dump())
        return {"message": "company created successfully", "id": company_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create-employee")  # company signup
async def add_employee(employee: UserCreate):
    try:
        print("employee->>", employee.model_dump())
        emp_id = await create_user(employee.model_dump())
        return {"message": "Employee created successfully", "id": emp_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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

    return await delete_department_service( company_id, filtered_dept)


@router.patch("/company/delete-subdepartment")
async def delete_subdepartment(payload: dict):
    data = payload.get("payload")
    if not data:
        return {"error": "Invalid request structure. Expected { payload: {...} }"}

    company_id = data["id"]
    filtered_subdept = data["filteredSubDept"]

    return await delete_subdepartment_service( company_id, filtered_subdept)


@router.get("/all-company")
async def get_all_company(user=Depends(require_role(["group","company"]))):
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
    return {
        "id": current_user["user_id"],
        "email": current_user["email"],
        "role": current_user["role"]
    }

@router.get("/single-user")
async def get_single_user(user_id: str):
    print(user_id)
    user =await get_user_by_id(user_id)
    return user


