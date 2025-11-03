# face.py
from fastapi import APIRouter, UploadFile, File , Form
from app.services.make_embade import get_face_embedding
from app.services.save_embedding import save_embedding
from app.services.one_to_n import one_to_n
from app.services.one_to_one import one_to_one
from app.services.delete_embedding_by_id import delete_embedding_by_id;
from fastapi import APIRouter, HTTPException
from app.core.databse import db

#............
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from datetime import datetime
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



@router.delete("/{user_id}")
async def delete_embedding(user_id: str):
    deleted = await delete_embedding_by_id(user_id)
    if deleted:
        return {"success": True, "message": f"Embedding with ID '{user_id}' deleted successfully."}
    else:
        raise HTTPException(status_code=404, detail=f"No embedding found with ID '{user_id}'")




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
async def verify_face(image: UploadFile = File(...),company_id: str = Form(...)):
    try:
        result = await one_to_n(image,company_id)
        return result
        # # Generate a unique filename with timestamp
        # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # file_path = SAVE_DIR / f"{timestamp}_{image.filename}"
        #
        # # Read uploaded file content
        # contents = await image.read()
        # # Save to disk
        # with open(file_path, "wb") as f:
        #     f.write(contents)
        #
        # print(f"Saved file: {file_path}")  # Optional: for backend log
        # print("live result--->>",result)
        # return {"success": result.match, "file_path": str(result.image_path)}
    except Exception as e:
        return {"match": False, "error": str(e)}