import streamlit as st
import os
from app import ask_gemini_about_document # Import your logic

st.set_page_config(layout="wide")
st.title("📄 Document AI Prototype with Gemini")

# --- THIS IS THE IMPORTANT NEW PART ---
# It securely gets your API key from Streamlit's secrets manager
# and configures the Google AI library.
import google.generativeai as genai
try:
    genai.configure(api_key=st.secrets["AIzaSyDG2QqJCeKF3X4_nhLZkxdIb5qdeXBR7xU"])
except Exception:
    st.error("API Key not found or configured incorrectly. Please add your GOOGLE_API_KEY to your Streamlit secrets.")
    st.stop() # Stops the app if the key is missing.
# --- END OF NEW PART ---


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
            # Call your backend function from app.py
            result = ask_gemini_about_document(prompt, file_path, mime_type)

        st.subheader("Analysis Result")
        st.markdown(result)

        # Clean up the uploaded file
        os.remove(file_path)
    else:
        st.error("Please upload a file and enter a prompt.")

