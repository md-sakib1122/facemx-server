import datetime
from app.core.databse import db
from typing import List, Dict

async def get_attendance(emp_id: str,company_id:str, start_date: datetime.date, end_date: datetime.date) -> List[Dict]:
    """
    Returns a list of attendance records per day for an employee
    Each record contains: date, entry_time, exit_time, status (present/absent)
    """
    result = []
    current_date = start_date

    while current_date <= end_date:
        # start and end datetime for the current day
        start_dt = datetime.datetime.combine(current_date, datetime.time.min)
        end_dt = datetime.datetime.combine(current_date, datetime.time.max)

        # fetch all records for this day
        records = await db["tracks"].find({
            "emp_id": emp_id,
            "company_id":company_id,
            "timestamp": {"$gte": start_dt, "$lte": end_dt}
        }).to_list(1000)  # adjust max as needed

        if records:
            times = [r["timestamp"] for r in records]
            entry_time = min(times).time()  # earliest time
            exit_time = max(times).time()   # latest time
            status = "Present"
        else:
            entry_time = None
            exit_time = None
            status = "Absent"

        result.append({
            "date": current_date,
            "entry_time": entry_time,
            "exit_time": exit_time,
            "status": status
        })

        current_date += datetime.timedelta(days=1)

    return result
