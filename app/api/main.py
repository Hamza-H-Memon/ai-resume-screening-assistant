from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import tempfile
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from app.scoring.criteria_extraction import extract_criteria
from app.parsing.resume_parser import parse_resume

app = FastAPI()


class JDRequest(BaseModel):
    jd_text: str


@app.get("/")
def read_root():
    return {"message": "Resume screening API is running"}


@app.post("/parse-jd")
def parse_jd(request: JDRequest):
    success, result = extract_criteria(request.jd_text)
    return {"success": success, "result": result}


@app.post("/parse-resume")
async def parse_resume_endpoint(resume: UploadFile = File(...)):
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir) / resume.filename
        content = await resume.read()
        tmp_path.write_bytes(content)

        success, result = parse_resume(str(tmp_path))

    return {"success": success, "result": result}