import streamlit as st
import pandas as pd
import json
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ocr_extract import extract_from_file

st.set_page_config(page_title="Invoice OCR", page_icon="🧾", layout="wide")
st.title("🧾 Invoice OCR Extractor")

st.sidebar.header("⚙️ Upload Invoice")
uploaded = st.sidebar.file_uploader("Upload PDF or Image", type=["pdf","png","jpg","jpeg","tiff","bmp"])

if uploaded:
    with st.spinner("🔍 Running OCR..."):
        result = extract_from_file(uploaded.read(), uploaded.name)

    fields = result["fields"]
    st.success("✅ Extraction Complete")

    # Display as metrics (cards)
    st.subheader("📌 Extracted Fields")
    cols = st.columns(2)
    for i, (k, v) in enumerate(fields.items()):
        with cols[i % 2]:
            st.metric(label=k.replace("_", " ").title(), value=v if v else "—")

    # Tabs
    tab1, tab2, tab3 = st.tabs(["📄 Full OCR Text", "🗂 JSON", "⬇️ Downloads"])

    with tab1:
        st.text_area("Raw OCR Text", result["full_text"], height=300)

    with tab2:
        st.json(result)

    with tab3:
        df = pd.DataFrame([fields])
        st.download_button("Download Fields (CSV)", df.to_csv(index=False).encode("utf-8"),
                           file_name=f"{uploaded.name}_fields.csv", mime="text/csv")
        st.download_button("Download Full Result (JSON)", json.dumps(result, indent=2).encode("utf-8"),
                           file_name=f"{uploaded.name}_ocr.json", mime="application/json")
else:
    st.info("👈 Upload a file from the sidebar to start.")
