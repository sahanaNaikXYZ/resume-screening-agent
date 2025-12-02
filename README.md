 Resume Screening Agent (VS Code Demo)

This project is a simple AI-assisted Resume Screening Tool that extracts text from resumes, compares it with a job description (JD), and ranks resumes based on matching keywords.  
It works in **local demo mode** without requiring an API key.

---

 Features

- Upload multiple PDF resumes  
- Extract text from:
  - Digital PDFs (using **pdfplumber**)
  - Scanned PDFs (using **Tesseract OCR**)  
- Extract text from DOCX resumes  
- Paste Job Description (JD)  
- Score and rank resumes based on keyword matching  
- Clean and simple Streamlit UI  
- Fully local — no external API required  

---

Tech Stack

- **Python**
- **Streamlit** – UI
- **pdfplumber** – PDF text extraction
- **pytesseract + Tesseract OCR** – scanned PDF extraction
- **python-docx** – DOCX parsing
- **NLP keyword matching** – scoring system

---

##  Project Structure

resume-screening-agent/
│── app.py
│── parsers.py
│── scorer.py
│── embeddings_client.py
│── utils.py
│── requirements.txt

yaml
Copy code

---

 How to Run the Project

Create a Virtual Environment
python -m venv .venv

yaml
Copy code

 Activate the Environment  
Windows PowerShell:
.venv\Scripts\activate

shell
Copy code

 Install Dependencies
pip install -r requirements.txt

bash
Copy code

Install Tesseract OCR (Required for scanned PDFs)
Download Windows installer:  
https://github.com/UB-Mannheim/tesseract/wiki

Set the path in `parsers.py`:

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

shell
Copy code

 Run the App
streamlit run app.py

yaml
Copy code

---

 How Resume Scoring Works

1. Extract text from resume  
2. Clean and convert to lowercase  
3. Convert JD to lowercase  
4. Match keywords  
5. Assign a similarity score  
6. Sort resumes from highest to lowest match  

---

 Future Enhancements

- Use OpenAI embeddings for smart semantic matching  
- Add multiple JD comparison  
- Add export to PDF/Excel  
- Add dashboard view  

---


Sahana Naik 
Resume Screening Agent – Demo Version  
