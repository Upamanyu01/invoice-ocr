# 🧾 Invoice OCR Extractor

This project provides a simple and interactive **Invoice OCR Extractor** built with **Python**, **Streamlit**, and **Gradio**. It allows users to upload invoices (PDF or image files) and extract key fields like invoice number, date, vendor name, total amount, and more using **Tesseract OCR**.

---

## Features

- ✅ Supports PDF, PNG, JPG, JPEG, TIFF, BMP file formats.
- ✅ Extracts main invoice fields:
  - Invoice Number
  - Invoice Date
  - Vendor Name
  - Customer Name & Address
  - Total Amount
  - Optional vehicle/model fields
- ✅ Provides full OCR text output.
- ✅ Downloads extracted data as CSV or JSON.
- ✅ Interactive UI with **Streamlit** and **Gradio**.

---

## Screenshots

- Streamlit interface:  
  - Upload sidebar  
  - Extracted fields displayed as metrics  
  - Tabs for full text, JSON, and download options  

- Gradio interface:  
  - File upload  
  - JSON code view of extracted fields  
  - Dataframe display  

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/Upamanyu01/invoice-ocr.git
cd invoice-ocr

2. **Create a virtual environment and activate it**

python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

3. **Install dependencies**
pip install -r requirements.txt

4 . **Install external dependencies**
Tesseract OCR: Download
https://github.com/tesseract-ocr/tesseract?utm_source=chatgpt.com

Make sure to update the path in ocr_extract.py:
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

Poppler (for PDF to image conversion): Download
Update the path in ocr_extract.py:
poppler_path = r"C:\Users\hp\Downloads\poppler-25.07.0\Library\bin"


5. **Run Project**
streamlit run app/streamlit_app.py
