from app.core.databse import db
from bson import ObjectId
from bson.errors import InvalidId
from typing import Dict
import logging

logger = logging.getLogger(__name__)


async def delete_company(company_id: str) -> Dict[str, any]:

    # Get collection references
    company_collection = db["users"]
    track_collection = db["tracks"]
    embedding_collection = db["embeddings"]
    locations_collection = db["company_locations"]

    try:
        obj_id = ObjectId(company_id)
    except InvalidId:
        logger.warning(f"Invalid company_id format: {company_id}")
        return {
            "success": False,
            "error": "Invalid company ID format"
        }

    try:

        company_result = await company_collection.delete_one({"_id": obj_id})

        if company_result.deleted_count == 0:
            logger.warning(f"Company not found: {company_id}")
            return {
                "success": False,
                "error": "Company not found"
            }

        # Delete all associated data
        employees_result = await company_collection.delete_many({
            "company_id": company_id,
            "role": "employee"
        })
        tracks_result = await track_collection.delete_many({"company_id": company_id})
        embeddings_result = await embedding_collection.delete_many({"company_id": company_id})
        locations_result = await locations_collection.delete_many({"company_id": company_id})

        deleted_counts = {
            "company": company_result.deleted_count,
            "employees": employees_result.deleted_count,
            "tracks": tracks_result.deleted_count,
            "embeddings": embeddings_result.deleted_count,
            "locations": locations_result.deleted_count
        }

        logger.info(
            f"Successfully deleted company {company_id}. "
            f"Deleted counts: {deleted_counts}"
        )

        return {
            "success": True,
            "deleted_counts": deleted_counts
        }

    except Exception as e:
        logger.error(f"Error deleting company {company_id}: {str(e)}", exc_info=True)
        return {
            "success": False,
            "error": f"Database error: {str(e)}"
        }