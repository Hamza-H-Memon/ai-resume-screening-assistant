import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st
import tempfile
from dotenv import load_dotenv
load_dotenv()

from app.scoring.criteria_extraction import extract_criteria
from app.parsing.resume_parser import parse_resume
from app.scoring.anonymizer import anonymize_text
from app.scoring.scorer import score_batch

st.title("AI Resume Screening Assistant")
st.write("Paste a job description, upload resumes, get a ranked shortlist.")

jd_text = st.text_area("Job description", height=200)

uploaded_files = st.file_uploader(
    "Upload resumes (PDF or DOCX)",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

anonymize = st.checkbox("Anonymize resumes before scoring")

if st.button("Run Screening"):
    success, criteria = extract_criteria(jd_text)
    st.write("Criteria extracted:", success)
    st.write(criteria)

    parsed_resumes = []

    if uploaded_files:
        with tempfile.TemporaryDirectory() as tmpdir:
            for uploaded_file in uploaded_files:
                tmp_path = Path(tmpdir) / uploaded_file.name
                tmp_path.write_bytes(uploaded_file.getvalue())

                parse_success, parse_result = parse_resume(str(tmp_path))
                if parse_success:
                    parsed_resumes.append((uploaded_file.name, parse_result))

        if anonymize:
            parsed_resumes = [(name, anonymize_text(text)) for name, text in parsed_resumes]

        st.write(f"Parsed {len(parsed_resumes)} of {len(uploaded_files)} resumes successfully.")

        if success and parsed_resumes:
            results = score_batch(parsed_resumes, criteria)

            st.subheader("Results")

            for r in results:
                st.write(f"**{r['filename']}** — Score: {r['overall_score']}")

                with st.expander("View evidence"):
                    for req in r["requirements"]:
                        status = req["status"]
                        st.write(f"**{req['requirement']}** — {status}")
                        if req["evidence"]:
                            st.caption(f"Evidence: \"{req['evidence']}\"")