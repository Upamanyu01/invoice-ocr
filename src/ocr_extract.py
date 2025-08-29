import io
from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract
import fitz  # PyMuPDF
from src.utils import load_config, get_logger

cfg = load_config()
logger = get_logger("ocr")

# ✅ Add Tesseract path explicitly
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# --- OCR Helper ---
def image_to_text(img: Image.Image) -> str:
    cfg_ocr = cfg["ocr"]
    config = f'--oem {cfg_ocr["tesseract_oem"]} --psm {cfg_ocr["tesseract_psm"]}'
    return pytesseract.image_to_string(img, config=config)

# --- PDF to text ---
def pdf_to_text(pdf_bytes: bytes):
    poppler_path = r"C:\Users\hp\Downloads\poppler-25.07.0\Library\bin"
    images = []

    try:
        images = convert_from_bytes(
            pdf_bytes,
            dpi=cfg["ocr"]["dpi"],
            fmt="png",
            poppler_path=poppler_path
        )
    except Exception as e:
        logger.warning(f"pdf2image failed: {e}. Falling back to PyMuPDF.")
        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            for page in doc:
                pix = page.get_pixmap(dpi=cfg["ocr"]["dpi"])
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                images.append(img)

    texts = [image_to_text(pg) for pg in images]
    return "\n".join(texts), images

# --- Image to text ---
def image_bytes_to_text(image_bytes: bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    return image_to_text(img), [img]

# --- Extract main fields ---
import re

def extract_main_fields(text: str):
    fields = {}

    # Invoice Number
    inv_match = re.search(r'Invoice Id[:\s]*#?([\w\-]+)', text, re.IGNORECASE)
    fields['invoice_number'] = inv_match.group(1) if inv_match else None

    # Vendor Name (first line of invoice)
    vendor_match = re.search(r'^(.*?)\s*\|', text)
    fields['vendor_name'] = vendor_match.group(1).strip() if vendor_match else None

    # Customer Name
    cust_match = re.search(r'Customer Details:\s*\nName[:\s]*(.+)', text, re.IGNORECASE)
    fields['customer_name'] = cust_match.group(1).strip() if cust_match else None

    # Customer Address
    addr_match = re.search(r'Address[:\s]*(.+)', text)
    fields['customer_address'] = addr_match.group(1).strip() if addr_match else None

    # Mobile Number
    mobile_match = re.search(r'Mobile Number[:\s]*(\+?\d+)', text)
    fields['customer_mobile'] = mobile_match.group(1) if mobile_match else None

    # Vehicle Number
    vehicle_match = re.search(r'Vehicle Number[:\s]*(\S+)', text)
    fields['vehicle_number'] = vehicle_match.group(1) if vehicle_match else None

    # Vehicle Model
    model_match = re.search(r'Model[:\s]*(.+)', text)
    fields['vehicle_model'] = model_match.group(1).strip() if model_match else None

    # Kms
    kms_match = re.search(r'Kms[:\s]*(\d+)', text)
    fields['vehicle_kms'] = kms_match.group(1) if kms_match else None

    # Total Amount
    total_match = re.search(r'Total Amount\s*[=:]\s*([\d,\.]+)', text, re.IGNORECASE)
    fields['total_amount'] = total_match.group(1).replace(',', '') if total_match else None

    return fields


# --- Main extraction function ---
def extract_from_file(file_bytes: bytes, filename: str):
    lower = filename.lower()
    if lower.endswith(".pdf"):
        text, images = pdf_to_text(file_bytes)
    else:
        text, images = image_bytes_to_text(file_bytes)

    # Extract only main fields
    main_fields = extract_main_fields(text)

    logger.info(f"Extracted main fields from {filename}: {main_fields}")
    return {
        "filename": filename,
        "fields": main_fields,
        "full_text": text,
        "num_pages": len(images),
    }
