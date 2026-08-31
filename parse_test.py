import pdfplumber

def extract_text_from_pdf(file_path):
    try:
        all_text = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    all_text.append(page_text)

        text = "\n".join(all_text)

        if not text:
            return False, "No extractable text found — this may be a scanned/image-based PDF."

        return True, text

    except Exception as e:
        return False, f"Error reading PDF: {e}"

success, result = extract_text_from_pdf("sample_resume.pdf")
print("Success:", success)
print(result)