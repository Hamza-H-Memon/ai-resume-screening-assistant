from dotenv import load_dotenv
load_dotenv()

from app.parsing.resume_parser import parse_resume
from app.scoring.criteria_extraction import extract_criteria

resume_success, resume_text = parse_resume("sample_resume.pdf")
print("Resume parsed:", resume_success)
print("Resume error/text:", resume_text)

with open("sample_jd.txt", "r", encoding="utf-8") as f:
    jd_text = f.read()

criteria_success, criteria = extract_criteria(jd_text)
print("Criteria extracted:", criteria_success)
print(criteria)

from app.scoring.scorer import score_resume

if resume_success and criteria_success:
    score_success, score_result = score_resume(resume_text, criteria)
    print("Scoring success:", score_success)
    print(score_result)