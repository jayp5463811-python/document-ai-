import streamlit as st
import google.generativeai as genai
import pypdf
import pandas as pd
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="GenAI Document Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- API CONFIGURATION ---
# --- API CONFIGURATION (Hardcoded for Hackathon) ---
# ⚠️ WARNING: Your key is public here. Delete this key after the hackathon.
GOOGLE_API_KEY = "AIzaSyBxpRh79rp0ThZqkEaB4wSkBcOwT_JA4Ig"
genai.configure(api_key=GOOGLE_API_KEY)
# --- HELPER FUNCTIONS ---
@st.cache_data
def load_data(file_path):
    if not os.path.exists(file_path):
        # This error will only show when running locally if my_data.csv is missing
        st.error(f"🚨 Error: The dataset file '{file_path}' was not found.")
        return None
    return pd.read_csv(file_path)

def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = pypdf.PdfReader(pdf_file)
        text = "".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())
        return text
    except Exception as e:
        st.error(f"⚠️ Error reading PDF file: {e}")
        return None

def get_gemini_response(prompt):
    try:
        model = genai.GenerativeModel('gemini-1.0-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"🧠 An error occurred with the AI model: {e}")
        return None

def find_relevant_context(query, dataframe, column_name):
    if dataframe is None or column_name not in dataframe.columns:
        return ""
    query_words = set(query.lower().split())
    relevant_rows = []
    for index, row in dataframe.iterrows():
        content = str(row[column_name]).lower()
        if any(word in content for word in query_words):
            row_context = ", ".join([f"{col}: {val}" for col, val in row.items() if col != 'Searchable_Details'])
            relevant_rows.append(row_context)
    return "\n".join(relevant_rows)

# --- UI & APP LOGIC ---
# For Streamlit Cloud, the file path will be relative to the root
df = load_data('my_data.csv')

st.title("📄 GenAI Document Analyzer")
st.markdown("Upload a document, ask questions, and get instant insights powered by Google Gemini.")

with st.sidebar:
    st.header("📤 Upload Your Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", label_visibility="collapsed")
    
    st.header("⚙️ Analysis Options")
    analysis_type = st.radio(
        "Choose an analysis type:",
        ("📝 Concise Summary", "🔑 Key Topics", "💡 Ask with Custom Data"),
        label_visibility="collapsed"
    )

    user_question = ""
    if analysis_type == "💡 Ask with Custom Data":
        user_question = st.text_input("Ask a question about your document:")

    analyze_button = st.button("Analyze Document", type="primary", use_container_width=True)

if analyze_button and uploaded_file is not None:
    with st.spinner("Analyzing your document..."):
        document_text = extract_text_from_pdf(uploaded_file)
        
        # --- FINAL FIX: Check if text was actually extracted ---
        if document_text and document_text.strip():
            final_prompt = ""
            if analysis_type == "💡 Ask with Custom Data" and user_question:
                relevant_info = find_relevant_context(user_question, df, 'Searchable_Details')
                final_prompt = f"""You are an AI assistant. Answer the user's QUESTION using the DOCUMENT TEXT and the CUSTOM KNOWLEDGE BASE provided below. Prioritize information from the knowledge base if it's relevant.
                ---CUSTOM KNOWLEDGE BASE---
                {relevant_info}
                ---DOCUMENT TEXT---
                {document_text}
                ---QUESTION---
                {user_question}"""
            elif analysis_type == "📝 Concise Summary":
                final_prompt = f"Provide a concise, easy-to-read summary of the following document:\n\n{document_text}"
            elif analysis_type == "🔑 Key Topics":
                final_prompt = f"List the top 5-7 key topics or themes from the following document in a bulleted list:\n\n{document_text}"

            if final_prompt:
                analysis_result = get_gemini_response(final_prompt)
                if analysis_result is not None and analysis_result.strip():
                    st.subheader("✨ Analysis Results")
                    st.markdown(analysis_result)
                else:
                    st.error("🚨 The AI returned a blank or invalid response. This can happen due to safety filters or the content of the PDF.")
            elif analysis_type == "💡 Ask with Custom Data":
                st.warning("Please ask a question to use this feature.")
        else:
            # --- FINAL FIX: Show an error if no text is found ---
            st.error("🚨 Could not extract any text from the uploaded PDF. Please try a different, text-based PDF file (not a scan or image).")

else:
    st.info("Please upload a document and select an analysis option from the sidebar.")
