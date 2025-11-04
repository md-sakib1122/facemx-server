from app.core.databse import db
import datetime

async def add_company_location(lat: float, lon: float, company_id: str, loc_name: str, rad: float) -> dict:
    """
    Save company location information into MongoDB.
    """
    collection = db["company_locations"]

    document = {
        "company_id": company_id,
        "loc_name": loc_name,
        "latitude": lat,
        "longitude": lon,
        "radius": rad,
        "created_at": datetime.datetime.utcnow(),
    }

    result = await collection.insert_one(document)
    return {"inserted_id": str(result.inserted_id)}
