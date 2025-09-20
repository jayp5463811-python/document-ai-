import streamlit as st
import os
from app import ask_gemini_about_document # Import your logic
import google.generativeai as genai

st.set_page_config(layout="wide")
st.title("📄 Document AI Prototype with Gemini")

# --- FINAL, MORE DETAILED DEBUGGING SECTION ---
st.subheader("⚙️ Debug Information")
try:
    # Step 1: Try to get the key from secrets.
    GOOGLE_API_KEY = st.secrets["AIzaSyCldcYxHTI7pL-MxIOhg2QfkPR8ayHHEbw"]
    st.success("✅ Step 1: Secret key named 'GOOGLE_API_KEY' was FOUND.")
    
    # Step 2: Display a part of the key for you to verify.
    # This helps confirm you pasted the correct value without showing the whole key.
    st.info(f"Step 2: Key value found starts with '{api_key_value[:5]}' and ends with '{api_key_value[-4:]}'. Please check if this matches your real key.")

    # Step 3: Try to configure the Google AI library with the key we found.
    genai.configure(api_key=api_key_value)
    st.success("✅ Step 3: Google AI configured successfully! Your app should now work below.")

except KeyError:
    st.error("❌ A 'KeyError' occurred. This means the secret's NAME is still wrong in your Streamlit settings. It must be exactly `GOOGLE_API_KEY`.")
    st.stop()
except Exception as e:
    st.error(f"❌ An unexpected error occurred during configuration: {e}")
    st.stop()
# --- END OF DEBUGGING SECTION ---


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

