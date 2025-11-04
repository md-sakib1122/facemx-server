from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import face,auth_route,attendance ,location_route
app = FastAPI(title="Face Verification API")


# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080","http://127.0.0.1:3000"],# React frontend origin
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

