from fastapi import FastAPI
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from app.routes import face,auth_route,attendance ,location_route
app = FastAPI(title="Face Verification API")
load_dotenv()

frontend_url = os.getenv("FRONTEND_URL")
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:3000",
]

if frontend_url:
    origins.append(frontend_url)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# Include face verification routes
app.include_router(face.router, prefix="/face", tags=["Face Recognition"])
app.include_router(auth_route.router, prefix="/auth", tags=["auth"])
app.include_router(attendance.router, prefix="/attendance", tags=["attendance"])
app.include_router(location_route.router, prefix="/location", tags=["location"])

@app.get("/")
def root():
    return {"message": "Face Verification API is running"}

