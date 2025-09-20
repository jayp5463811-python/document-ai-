import streamlit as st
import os
from app import ask_gemini_about_document # Import your logic
import google.generativeai as genai

st.set_page_config(layout="wide")
st.title("📄 Document AI Prototype with Gemini")

# --- NEW DEBUGGING SECTION ---
# This code will check if the secret is available and tell us.
st.subheader("⚙️ Debug Information")
if "GOOGLE_API_KEY" in st.secrets:
    st.success("✅ Secret key was FOUND by the app.")
else:
    st.error("❌ Secret key was NOT FOUND by the app.")
    st.info("This means the name in your app's 'Secrets' settings is probably wrong. It must be exactly GOOGLE_API_KEY.")
    st.stop() # Stop the app here if the key isn't found.
# --- END OF DEBUGGING SECTION ---

# --- Configure the API using the secret ---
try:
    genai.configure(api_key=st.secrets["AIzaSyCldcYxHTI7pL-MxIOhg2QfkPR8ayHHEbw"])
    st.success("✅ Google AI configured successfully!")
except Exception as e:
    st.error(f"An error occurred when trying to configure the API: {e}")
    st.stop()

# --- The rest of your app's user interface ---
st.subheader("💬 Ask Your Document a Question")

# Create a directory for uploads if it doesn't exist
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# File uploader
uploaded_file = st.file_uploader("Upload your document (PDF, PNG, JPG)", type=["pdf", "png", "jpg"])

# Text input for the prompt
prompt = st.text_input("What do you want to know about the document?")

if st.button("Analyze Document"):
    if uploaded_file is not None and prompt:
        file_path = os.path.join("uploads", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner("Analyzing your document..."):
            mime_type = uploaded_file.type
            result = ask_gemini_about_document(prompt, file_path, mime_type)

        st.subheader("Analysis Result")
        st.markdown(result)
        os.remove(file_path)
    else:
        st.error("Please upload a file and enter a prompt.")

