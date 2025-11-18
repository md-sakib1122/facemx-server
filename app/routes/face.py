# face.py
from fastapi import APIRouter, UploadFile, File , Form
from app.services.make_embade import get_face_embedding
from app.services.save_embedding import save_embedding
from app.services.one_to_n import one_to_n
from app.services.one_to_one import one_to_one
from app.services.delete_embedding_by_id import delete_embedding_by_id;
from fastapi import APIRouter, HTTPException
from app.core.databse import db
from app.liveness.verify import  detect_liveness
#............
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from datetime import datetime
import numpy as np
import cv2
#............


router = APIRouter(tags=["face"])



@router.post("/one-one")
async def one_one(img1: UploadFile = File(...), img2: UploadFile = File(...)):
    result = await one_to_one(img1, img2)
    return result


@router.post("/save-embed")
async def save_embed(img1: UploadFile = File(...), file_path: str = Form(...),emp_id: str = Form(...),notes: str = Form(...), company_id :str = Form(...)):
    result = await get_face_embedding(img1)
    await  save_embedding(result,file_path,emp_id,notes,company_id)
    return {"message": "Embedding saved successfully"}



@router.post("/one-to-n")
async def one_to_n_route(img1: UploadFile = File(...),company_id: str = Form(...) ):
    print("company_id", company_id)
    result = await one_to_n(img1,company_id)
    return result



@router.delete("/delete-embed")
async def delete_embedding(data: dict):
    try:
        print("data", data)
        user_id = data["emp_id"]
        company_id = data["company_id"]
        deleted = await delete_embedding_by_id(user_id, company_id)
        if deleted:
            return {"success": True, "message": f"Embedding for employee '{user_id}' deleted successfully."}
        else:
            raise HTTPException(status_code=404, detail=f"No embedding found for employee '{user_id}'")
    except KeyError:
        raise HTTPException(status_code=400, detail="Missing required fields: emp_id and company_id")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





@router.post("/embeddings")
async def get_all_embeddings(data: dict):
    try:
        company_id = data["company_id"]
        cursor = db.embeddings.find(
            {"company_id": company_id},  # 🟢 filter
            {"_id": 0, "emp_id": 1, "image_path": 1, "notes": 1}  # 🟢 projection
        )

        data = [doc async for doc in cursor]

        if not data:
            return {"count": len(data), "embeddings": data}

        return {"count": len(data), "embeddings": data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    #.....................from


# Directory to save uploaded images
SAVE_DIR = Path("uploaded_faces")
SAVE_DIR.mkdir(exist_ok=True)

@router.post("/verify-live")
async def verify_face(image: UploadFile = File(...), company_id: str = Form(...)):
    try:
        # Read file ONCE
        contents = await image.read()
        np_img = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        if img is None:
            print(" img error hit korce")
            return {"status": "error", "message": "Invalid image file"}

        # Detect liveness (pass numpy img)
        result_live = await detect_liveness(img)

        if result_live["result"] == "RealFace":
            # Run recognition
            print(" liveness result is -->>RealFace")
            result = await one_to_n(img, company_id)
            print("1 to N result ->>", result)
            return result
        else:
            print(" liveness result is -->>FakeFace")
            return {"match": False, "live":False}

    except Exception as e:
        print(" exception hit korce")
        return {"match": False, "error": str(e)}




#
# @router.post("/verify-live")
# async def verify_face(image: UploadFile = File(...), company_id: str = Form(...)):
#     response = {"match": False, "live": False, "data": None, "error": None}
#     try:
#         contents = await image.read()
#         np_img = np.frombuffer(contents, np.uint8)
#         img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
#         if img is None:
#             response["error"] = "Invalid image file"
#             return response
#
#         result_live = await detect_liveness(img)
#         if result_live["result"] == "RealFace":
#             one_to_n_result = await one_to_n(img, company_id)
#             response.update({
#                 "match": one_to_n_result.get("match", False),
#                 "live": True,
#                 "data": one_to_n_result.get("data")
#             })
              #return response
#         else:
#             response["live"] = False
#             return response
#     except Exception as e:
#          raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Face recognition service temporarily unavailable"
#         )
#

