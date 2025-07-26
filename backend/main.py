
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid, os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
job_results = {}

@app.get("/")
def read_root():
    return {"message": "Welcome to GeM Watcher Backend"}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    job_id = str(uuid.uuid4())
    file_location = os.path.join(UPLOAD_DIR, f"{job_id}.pdf")
    
    with open(file_location, "wb") as f:
        f.write(await file.read())
    
    job_results[job_id] = {"status": "processed", "summary": f"Fake summary of {file.filename}"}
    return {"job_id": job_id, "filename": file.filename}

@app.get("/job/{job_id}")
def get_job_result(job_id: str):
    result = job_results.get(job_id)
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Job not found")
