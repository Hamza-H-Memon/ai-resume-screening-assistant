from dotenv import load_dotenv
load_dotenv()

from app.scoring.criteria_extraction import extract_criteria
from app.scoring.scorer import score_resume
from app.scoring.anonymizer import anonymize_text

resume_template = """{name}
Business Analyst

Profile
Detail-oriented Business Analyst with 4 years of experience translating business requirements into clear specifications and supporting data-driven decision making.

Experience
Business Analyst | Meridian Consulting Group | 2022 - Present
Analyzed client business processes and identified process improvement opportunities across 3 departments.
Translated stakeholder requirements into clear functional specifications for delivery teams.
Presented findings and recommendations directly to client leadership on a quarterly basis.

Junior Business Analyst | Hartwell & Co. | 2020 - 2022
Supported senior analysts with reporting, documentation, and requirements gathering.
Built and maintained Excel-based tracking dashboards for client engagements.

Education
B.A. in Business Administration, State University, 2020
"""

resume_original = resume_template.format(name="Emily Sullivan")
resume_variant = resume_template.format(name="Lakisha Washington")

with open("data/sample_jds/sample_jd.txt", "r", encoding="utf-8") as f:
    jd_text = f.read()

_, criteria = extract_criteria(jd_text)


def print_result(label, success, result):
    if not success:
        print(f"{label}: FAILED - {result}")
        return
    print(f"{label}: {result['overall_score']}")
    for req in result["requirements"]:
        print(f"  {req['status']}: {req['requirement']}")


success, result = score_resume(resume_original, criteria)
print_result("Emily Sullivan", success, result)

success, result = score_resume(resume_variant, criteria)
print_result("\nLakisha Washington", success, result)

anon_original = anonymize_text(resume_original)
anon_variant = anonymize_text(resume_variant)

success, result = score_resume(anon_original, criteria)
print_result("\nAnonymized Emily Sullivan", success, result)

success, result = score_resume(anon_variant, criteria)
print_result("\nAnonymized Lakisha Washington", success, result)