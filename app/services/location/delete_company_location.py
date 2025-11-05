from bson import ObjectId
from app.core.databse import db
async def delete_company_location(location_id: str):
    try:
        # Ensure the provided ID is valid
        location_collection = db["company_locations"]
        if not ObjectId.is_valid(location_id):
            return None

        result = await location_collection.delete_one({"_id": ObjectId(location_id)})

        # Check if a document was actually deleted
        if result.deleted_count == 0:
            return None

        return True
    except Exception as e:
        raise e