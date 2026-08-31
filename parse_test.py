import pdfplumber
import docx

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


def extract_text_from_docx(file_path):
    try:
        document = docx.Document(file_path)
        paragraphs = []
        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                paragraphs.append(paragraph.text)

        text = "\n".join(paragraphs)

        if not text:
            return False, "No text content found in DOCX."

        return True, text

    except Exception as e:
        return False, f"Error reading DOCX: {e}"

success, result = extract_text_from_docx("sample_resume.docx")
print("Success:", success)
print(result)