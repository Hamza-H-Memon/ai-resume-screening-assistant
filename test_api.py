import requests

with open("sample_jd.txt", "r", encoding="utf-8") as f:
    jd_text = f.read()

files = [
    ("resumes", ("sample_resume.pdf", open("sample_resume.pdf", "rb"), "application/pdf")),
    ("resumes", ("sample_resume.docx", open("sample_resume.docx", "rb"), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")),
]

data = {"jd_text": jd_text}

response = requests.post("http://127.0.0.1:8000/score-resumes", data=data, files=files)

print(response.status_code)
print(response.json())