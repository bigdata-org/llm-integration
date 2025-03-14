
import streamlit as st
import requests
import json

#API_BASE_URL = "http://localhost:8000"

API_BASE_URL = "https://case-798800248787.us-central1.run.app"

# Streamlit UI Design
st.set_page_config(page_title="PDF Analyzer", layout="wide")
st.title("📄 Pytract PDF Analyzer with AI")

# Sidebar for Upload and Select
st.sidebar.header("Upload or Select PDF")

# Upload PDF Section
uploaded_file = st.sidebar.file_uploader("Upload a PDF", type=["pdf"])
if uploaded_file:
    files = {"file": uploaded_file.getvalue()}
    response = requests.post(f"{API_BASE_URL}/upload_pdf", files=files)
    if response.status_code == 200:
        st.sidebar.success(f"Uploaded: {uploaded_file.name}")
    else:
        st.sidebar.error("Error uploading file.")

# Select Parsed PDF Section
parsed_pdfs = requests.get(f"{API_BASE_URL}/select_pdfcontent").json().get("parsed_pdfs", [])
selected_pdf = st.sidebar.radio("Select a Parsed PDF", parsed_pdfs)

# Main Panel for Functionality
st.header(f"Selected PDF: {selected_pdf}" if selected_pdf else "Select a PDF to Continue")

if selected_pdf:
    tab1, tab2 = st.tabs(["📋 Summarize", "❓ Q&A"])

    with tab1:
        st.subheader("Summary")
        if st.button("Generate Summary"):
            data = {"document_id": selected_pdf}
            response = requests.post(f"{API_BASE_URL}/summarize", data=data)
            if response.status_code == 200:
                st.success(response.json().get("summary"))
            else:
                st.error("Error generating summary.")

    with tab2:
        st.subheader("Ask a Question")
        question = st.text_input("Enter your question:")
        if st.button("Ask"):
            data = {"document_id": selected_pdf, "question": question}
            response = requests.post(f"{API_BASE_URL}/ask_question", data=data)
            if response.status_code == 200:
                st.success(response.json().get("answer"))
            else:
                st.error("Error generating answer.")

# Style Enhancements
st.markdown("""
    <style>
        .stButton>button { width: 100%; border-r~adius: 10px; background-color: #4CAF50; color: white; }
        .stTextInput>div>div>input { border-radius: 10px; border: 2px solid #4CAF50; }
        .stRadio { border: 1px solid #4CAF50; border-radius: 10px; padding: 10px; }
    </style>
""", unsafe_allow_html=True)



