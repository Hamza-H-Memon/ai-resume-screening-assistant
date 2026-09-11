from dotenv import load_dotenv
load_dotenv()

from pathlib import Path
from app.parsing.resume_parser import parse_resume
from app.scoring.criteria_extraction import extract_criteria
from app.scoring.scorer import score_batch

resume_files = list(Path("data/sample_resumes").glob("*.pdf")) + list(Path("data/sample_resumes").glob("*.docx"))
jd_files = list(Path("data/sample_jds").glob("*.txt"))

parsed_resumes = []
for resume_path in resume_files:
    success, text = parse_resume(str(resume_path))
    if success:
        parsed_resumes.append((resume_path.name, text))

print(f"Parsed {len(parsed_resumes)} of {len(resume_files)} resumes successfully.\n")

for jd_path in jd_files:
    with open(jd_path, "r", encoding="utf-8") as f:
        jd_text = f.read()

    criteria_success, criteria = extract_criteria(jd_text)
    if not criteria_success:
        print(f"Skipping {jd_path.name} — criteria extraction failed")
        continue

    print(f"=== {jd_path.name} ===")
    results = score_batch(parsed_resumes, criteria)
    for r in results:
        if "error" in r:
            print(f"  {r['filename']} - FAILED: {r['error']}")
        else:
            print(f"  {r['filename']} - {r['overall_score']}")
    print()

print("=== DETAILED VIEW: sample_jd.txt tied resumes ===")

with open("data/sample_jds/sample_jd.txt", "r", encoding="utf-8") as f:
    jd_text = f.read()

_, criteria = extract_criteria(jd_text)

tied_filenames = [
    "business-analyst-resume-example.pdf",
    "business-systems-analyst-resume-example.pdf",
    "salesforce-business-analyst-resume-example.pdf",
    "senior-business-analyst-resume-example.pdf",
]

tied_resumes = [(name, text) for name, text in parsed_resumes if name in tied_filenames]
detailed_results = score_batch(tied_resumes, criteria)

for r in detailed_results:
    print(f"\n--- {r['filename']} (score: {r['overall_score']}) ---")
    for req in r["requirements"]:
        print(f"  {req['status']}: {req['requirement']}")
        if req["evidence"]:
            print(f"    Evidence: {req['evidence'][:150]}")