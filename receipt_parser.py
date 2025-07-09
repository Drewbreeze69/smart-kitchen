import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import re
from tabulate import tabulate
import os
import glob

# ---------- CONFIG ----------
RECEIPT_FOLDER = "/Users/andrewlindsay/Documents/Receipt folder"  # ✅ ← Updated folder path

# ---------- Load Latest PDF ----------
def find_latest_pdf(folder):
    pdfs = glob.glob(os.path.join(folder, "*.pdf"))
    if not pdfs:
        print("❌ No PDF files found in the folder.")
        exit()
    latest_pdf = max(pdfs, key=os.path.getmtime)
    print(f"📄 Found latest receipt: {os.path.basename(latest_pdf)}")
    return latest_pdf

# ---------- OCR Processing ----------
def extract_text_from_pdf(pdf_path):
    print("🔍 Converting PDF to images...")
    pages = convert_from_path(pdf_path, dpi=300)
    text = ''
    for page in pages:
        text += pytesseract.image_to_string(page) + '\n'
    return text

# ---------- Receipt Line Parsing ----------
def parse_items(text):
    lines = text.split('\n')
    items = []
    manual_review = []

    item_pattern = re.compile(r"^(\d+)?\s?(.+?)\s+£\d")  # e.g., "2 Flapjack Bars £3.50"

    for line in lines:
        line = line.strip()
        if not line or '£' not in line:
            continue

        match = item_pattern.match(line)
        if match:
            qty = match.group(1)
            name = match.group(2).strip().lower()
            try:
                qty = int(qty) if qty else 1
                items.append((name, qty))
            except:
                manual_review.append(line)
        else:
            # Filter noise: ignore Sainsbury's headers, totals, etc.
            if any(x in line.lower() for x in ['£', 'g', 'ml', 'kg']) and not line.lower().startswith("sainsbury"):
                manual_review.append(line)
    return items, manual_review

# ---------- Display Results ----------
def display_results(items, manual_review):
    print("\n✅ Parsed Items:\n")
    if items:
        print(tabulate(items, headers=["Item", "Quantity"], tablefmt="pretty"))
    else:
        print("No items parsed successfully.")

    if manual_review:
        print("\n⚠️  Items for Manual Review:\n")
        for line in manual_review:
            print("- " + line)

# ---------- Main ----------
def main():
    pdf_path = find_latest_pdf(RECEIPT_FOLDER)
    text = extract_text_from_pdf(pdf_path)
    items, manual_review = parse_items(text)
    display_results(items, manual_review)

if __name__ == "__main__":
    main()
