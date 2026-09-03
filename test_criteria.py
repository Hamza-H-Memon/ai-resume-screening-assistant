from dotenv import load_dotenv
load_dotenv()

from app.scoring.criteria_extraction import extract_criteria

with open("sample_jd.txt", "r", encoding="utf-8") as f:
    jd_text = f.read()

success, result = extract_criteria(jd_text)
print("Success:", success)
print(result)