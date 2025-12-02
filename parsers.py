import io
import pdfplumber
import docx
from pdf2image import convert_from_bytes
import pytesseract

# -----------------------------------------------------
# SET YOUR TESSERACT PATH HERE  (VERY IMPORTANT)
# -----------------------------------------------------
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# -----------------------------------------------------
# MAIN ROUTER FUNCTION
# -----------------------------------------------------
def extract_text_from_file(file_like):
    filename = getattr(file_like, "name", "uploaded_file")
    lower = filename.lower()

    if lower.endswith(".pdf"):
        return extract_pdf(file_like)

    if lower.endswith(".docx"):
        return extract_docx(file_like)

    # assume .txt or other text file
    try:
        raw = file_like.read()
        if isinstance(raw, bytes):
            raw = raw.decode(errors="ignore")
        return raw
    except:
        return ""


# -----------------------------------------------------
# PDF EXTRACTION (Digital + Scanned)
# -----------------------------------------------------
def extract_pdf(file_like):
    pdf_bytes = file_like.read()

    # 1) Try digital PDF extraction
    text_chunks = []
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_chunks.append(page_text)
    except Exception as e:
        print("pdfplumber error:", e)

    extracted_text = "\n".join(text_chunks).strip()

    # 2) If digital extraction is empty → use OCR
    if not extracted_text:
        try:
            images = convert_from_bytes(pdf_bytes)
            ocr_output = []
            for img in images:
                text = pytesseract.image_to_string(img)
                if text:
                    ocr_output.append(text)
            extracted_text = "\n".join(ocr_output).strip()
        except Exception as e:
            print("OCR Error:", e)
            extracted_text = ""

    # DEBUG OUTPUT - PRINT FIRST 300 CHARACTERS
    print("EXTRACTED TEXT (DEBUG):", extracted_text[:300])

    return extracted_text


# -----------------------------------------------------
# DOCX EXTRACTION
# -----------------------------------------------------
def extract_docx(file_like):
    try:
        doc = docx.Document(io.BytesIO(file_like.read()))
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        print("DOCX error:", e)
        return ""
