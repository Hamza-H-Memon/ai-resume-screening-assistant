from app.parsing.resume_parser import parse_resume

success, result = parse_resume("data/sample_resumes/sample_resume.pdf")
print("Success:", success)