from app.core.databse import db
from bson import ObjectId


employee_collection = db["users"]

async def update_employee_locations(employee_id: str, locations: list):

    if not ObjectId.is_valid(employee_id):
        return None

    # Prepare the update
    update_query = {"$set": {"locations": locations}}

    # Update the document
    result = await employee_collection.find_one_and_update(
        {"_id": ObjectId(employee_id)},
        update_query,
        return_document=True  # Return the updated document
    )

    if result:
        # Convert ObjectId to str for JSON serialization
        result["_id"] = str(result["_id"])
    return result
