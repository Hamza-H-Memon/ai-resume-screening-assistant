from fastapi import FastAPI
from pydantic import BaseModel

from dotenv import load_dotenv
load_dotenv()

from app.scoring.criteria_extraction import extract_criteria

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