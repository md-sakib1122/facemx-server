from app.core.databse import db
import datetime
from fastapi import APIRouter, HTTPException, Response,Depends,Body
from app.services.attendance.save_tracking import save_tracking
from app.models.attendanceModel import  AttendanceRequest
from app.services.attendance.get_attendance import get_attendance
router = APIRouter(tags=["attendance"])

@router.post("/save-track")
async def track_and_save(data:dict):
    try:
      emp_id = data["emp_id"]
      company_id = data["company_id"]
      result = await save_tracking(emp_id, data["match_score"],company_id, data["current_lat"], data["current_lon"] , data["dist"])
      return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.post("/get-attendance")
async def attendance_report(req: AttendanceRequest):
    start = datetime.datetime.strptime(req.start_date, "%Y-%m-%d").date()
    end = datetime.datetime.strptime(req.end_date, "%Y-%m-%d").date()
    print("emp id:",req.emp_id)
    data = await get_attendance(req.emp_id,req.company_id, start, end)
    print("returned data",data)
    return data
