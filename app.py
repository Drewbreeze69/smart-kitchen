import streamlit as st
import os
from receipt_parser import extract_text_from_pdf, parse_items

RECEIPT_FOLDER = "/Users/andrewlindsay/Documents/Receipt folder"

def find_latest_pdf(folder):
    pdfs = [f for f in os.listdir(folder) if f.endswith(".pdf")]
    if not pdfs:
        return None
    latest = max(pdfs, key=lambda f: os.path.getmtime(os.path.join(folder, f)))
    return os.path.join(folder, latest)

st.set_page_config(page_title="Smart Kitchen Parser", page_icon="🥬")

st.title("🥕 Smart Kitchen - Receipt Parser")
st.markdown("Upload a receipt to see your ingredients!")

# Load latest PDF
pdf_path = find_latest_pdf(RECEIPT_FOLDER)

if pdf_path:
    st.success(f"Found latest receipt: `{os.path.basename(pdf_path)}`")

    if st.button("📥 Parse Receipt"):
        with st.spinner("Reading and processing receipt..."):
            text = extract_text_from_pdf(pdf_path)
            items, review = parse_items(text)

        st.subheader("✅ Parsed Items")
        if items:
            for name, qty in items:
                st.markdown(f"- **{qty}×** {name}")
        else:
            st.write("No items parsed.")

        if review:
            st.subheader("⚠️ Manual Review Needed")
            for line in review:
                st.text(line)
else:
    st.warning("No PDF receipts found in the Receipt folder.")
