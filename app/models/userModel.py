from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from app.models.locationModel import  Location
class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str
    # company
    parent: Optional[str] = None
    department: List[str] = Field(default_factory=list)
    subdepartment: List[str] = Field(default_factory=list)
    company_code: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    fax: Optional[str] = None
    phone: Optional[str] = None
    tax_no: Optional[str] = None
    country: Optional[str] = None
    abbreviate_name: Optional[str] = None
    #company
    #employe base info
    userDept: Optional[str] = None
    userSubDept: Optional[str] = None
    emp_id: Optional[str] = None
    group_id: Optional[str] = None
    company_id: Optional[str] = None
    locations: List[Location] = Field(default_factory=list)

    #emp base info

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    parent: Optional[str] = None
    department: Optional[List[str]] = None
    subdepartment: Optional[List[str]] = None
    password: Optional[str] = None

# Schemas for the update endpoints
class AddDepartmentModel(BaseModel):
    id: str
    department: str  # single string

class SubDepartmentUpdate(BaseModel):
    id: str
    subdepartment: str

class UserDB(UserBase):
    id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True

