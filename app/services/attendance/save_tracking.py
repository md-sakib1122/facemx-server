import datetime
from app.core.databse import db

async def save_tracking(emp_id: str, match_score: str, company_id: str):
    collection = db["tracks"]
    print("Company Id:", company_id)
    document = {
        "emp_id": emp_id,
        "company_id": company_id,
        "match_score": match_score,
        "timestamp": datetime.datetime.now()
    }
    result = await collection.insert_one(document)
    return str(result.inserted_id)


