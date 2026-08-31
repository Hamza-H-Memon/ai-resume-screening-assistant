import pdfplumber

def extract_text_from_pdf(file_path):
    all_text = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                all_text.append(page_text)
    return "\n".join(all_text)

result = extract_text_from_pdf("sample_resume.pdf")
print(result)