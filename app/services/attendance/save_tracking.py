import datetime

from sympy import Number

from app.core.databse import db

async def save_tracking(emp_id: str, match_score: str, company_id: str , current_lat: Number, current_lon: Number, dist: Number) -> dict:
    collection = db["tracks"]
    print("Company Id:", company_id)
    document = {
        "emp_id": emp_id,
        "company_id": company_id,
        "match_score": match_score,
        "timestamp": datetime.datetime.now(),
        "current_lat": current_lat,
        "current_lon": current_lon,
        "dist": dist,
    }
    result = await collection.insert_one(document)
    return str(result.inserted_id)


