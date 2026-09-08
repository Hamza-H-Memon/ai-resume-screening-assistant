from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
import tempfile
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from app.scoring.criteria_extraction import extract_criteria
from app.parsing.resume_parser import parse_resume
from app.scoring.scorer import score_batch

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


@app.post("/score-resumes")
async def score_resumes(
    jd_text: str = Form(...),
    resumes: list[UploadFile] = File(...)
):
    criteria_success, criteria = extract_criteria(jd_text)
    if not criteria_success:
        return {"success": False, "error": "Failed to extract criteria from JD"}

    parsed_resumes = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for resume in resumes:
            tmp_path = Path(tmpdir) / resume.filename
            content = await resume.read()
            tmp_path.write_bytes(content)

            parse_success, parse_result = parse_resume(str(tmp_path))
            if parse_success:
                parsed_resumes.append((resume.filename, parse_result))

    if not parsed_resumes:
        return {"success": False, "error": "No resumes could be parsed"}

    results = score_batch(parsed_resumes, criteria)
    return {"success": True, "results": results}