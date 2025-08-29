import re
from dateutil import parser as dateparser

def normalize_amount(s: str):
    if not s:
        return None
    s = s.replace(",", "").replace(" ", "")
    s = re.sub(r"^(USD|INR|Rs.?|₹|\$)", "", s, flags=re.IGNORECASE).strip()
    try:
        return float(s)
    except Exception:
        return None

def extract_first_date(text: str, date_patterns):
    for pat in date_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            try:
                return dateparser.parse(m.group(0), fuzzy=True).strftime("%Y-%m-%d")
            except Exception:
                pass
    return None

def parse_invoice_text(full_text: str, cfg: dict):
    text = re.sub(r"[ \t]+", " ", full_text)
    lines = [ln.strip() for ln in full_text.splitlines() if ln.strip()]
    results = {}

    # Invoice number
    for pat in cfg["patterns"]["invoice_number"]:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            results["invoice_number"] = m.group(1).strip()
            break

    # Dates
    results["invoice_date"] = extract_first_date(text, cfg["patterns"]["date_patterns"])
    results["due_date"] = None  # extend if needed

    # Amounts
    for field in ["subtotal", "tax", "total"]:
        for pat in cfg["patterns"][field]:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                results[field] = normalize_amount(m.group(1))
                break

    # Vendor name
    results["vendor_name"] = lines[0] if lines else None

    # Bill To (simple heuristic)
    bill_to = None
    for i, ln in enumerate(lines):
        if re.search(r"\b(bill(?:ed)?\s*to|invoice\s*to|ship\s*to)\b", ln, re.IGNORECASE):
            block = lines[i+1:i+4]
            bill_to = " ".join(block).strip() if block else None
            break
    results["bill_to"] = bill_to

    return results
