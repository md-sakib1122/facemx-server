from app.core.databse import db


async def get_company_location(company_id: str) -> list:
    collection = db["company_locations"]

    try:
        cursor = collection.find({"company_id": company_id})
        locations = await cursor.to_list(length=None)

        # Convert ObjectId to string for JSON serialization
        for loc in locations:
            loc["id"] = str(loc["_id"])
            del loc["_id"]

        return locations

    except Exception as e:
        raise Exception(f"Database error: {e}")
