from fastapi import APIRouter, HTTPException
from app.services.location.add_compnay_loc_service import add_company_location
from app.services.location.get_company_location import get_company_location
router = APIRouter(tags=["location"])

@router.post("/add-company-location")
async def add_company_loc(data: dict):
    try:
        lat = float(data["lat"])
        lon = float(data["lon"])
        company_id = data["company_id"]
        loc_name = data["loc_name"]
        rad = float(data["rad"])

        result = await add_company_location(lat, lon, company_id, loc_name, rad)
        return {"success": True, "message": "Location saved successfully", "data": result}
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing field: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/get-company-location")
async def get_company_loc(data: dict):
    try:
        company_id = data.get("company_id")
        if not company_id:
            raise HTTPException(status_code=400, detail="Missing field: company_id")

        result = await get_company_location(company_id)
        if result is None:
            return {"success": False, "message": "No location found for this company"}

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))