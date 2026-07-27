from fastapi import FastAPI

from app.api.resumes import router as resumes_router
from app.db import check_db_connection

# This creates the FastAPI "application" object.
app = FastAPI(title="Job Application Assistant API")

# Mounts every endpoint defined in app/api/resumes.py under this app.
# Because the router itself has prefix="/resumes", the upload endpoint
# becomes POST /resumes/upload and the list endpoint becomes GET /resumes/.
app.include_router(resumes_router)


@app.get("/")
def read_root():
    return {"status": "ok", "message": "Job Application Assistant API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/db-health")
def db_health_check():
    if check_db_connection():
        return {"status": "connected"}
    return {"status": "disconnected"}
