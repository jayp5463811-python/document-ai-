import streamlit as st
import os
from app import ask_gemini_about_document # Import your logic

st.set_page_config(layout="wide")
st.title("📄 Document AI Prototype with Gemini")

# Create a directory for uploads if it doesn't exist
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# File uploader
uploaded_file = st.file_uploader("Upload your document (PDF, PNG, JPG)", type=["pdf", "png", "jpg"])

# Text input for the prompt
prompt = st.text_input("What do you want to know about the document?")

if st.button("Analyze Document"):
    if uploaded_file is not None and prompt:
        # Save the file temporarily
        file_path = os.path.join("uploads", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Show a spinner while processing
        with st.spinner("Analyzing your document... This may take a moment for PDFs."):
            # Get the MIME type
            mime_type = uploaded_file.type
            # Call your backend function
            result = ask_gemini_about_document(prompt, file_path, mime_type)

        st.subheader("Analysis Result")
        st.markdown(result)

        # Clean up the uploaded file
        os.remove(file_path)
    else:
        st.error("Please upload a file and enter a prompt.")
