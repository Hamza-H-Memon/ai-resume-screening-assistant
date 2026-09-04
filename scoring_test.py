from dotenv import load_dotenv
load_dotenv()

from app.parsing.resume_parser import parse_resume
from app.scoring.criteria_extraction import extract_criteria
from app.scoring.scorer import score_batch

with open("sample_jd.txt", "r", encoding="utf-8") as f:
    jd_text = f.read()

criteria_success, criteria = extract_criteria(jd_text)
print("Criteria extracted:", criteria_success)
print(criteria)

pdf_success, pdf_text = parse_resume("sample_resume.pdf")
docx_success, docx_text = parse_resume("sample_resume.docx")

resumes = []
if pdf_success:
    resumes.append(("sample_resume.pdf", pdf_text))
if docx_success:
    resumes.append(("sample_resume.docx", docx_text))

if criteria_success and resumes:
    results = score_batch(resumes, criteria)
    for r in results:
        print(r["filename"], "-", r["overall_score"])