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
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
except (FileNotFoundError, KeyError):
    st.error("🚨 API Key not found! Please add it to your Streamlit secrets.")
    st.stop()

# --- HELPER FUNCTIONS ---
@st.cache_data
def load_data(file_path):
    if not os.path.exists(file_path):
        st.error(f"🚨 Error: The dataset file '{file_path}' was not found. Please run 'python dataset.py' first.")
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
        return None # Return None on error

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
        
        if document_text:
            final_prompt = ""
            if analysis_type == "💡 Ask with Custom Data" and user_question:
                # --- START DEBUGGING ---
                st.info("Searching for context in custom data...")
                relevant_info = find_relevant_context(user_question, df, 'Searchable_Details')
                
                if relevant_info:
                    st.success(f"Found context for '{user_question}'!")
                    with st.expander("See context found"):
                        st.text(relevant_info)
                else:
                    st.warning(f"Could not find any context for '{user_question}' in the custom data.")
                # --- END DEBUGGING ---

                final_prompt = f"""You are an AI assistant. Answer the user's QUESTION using the DOCUMENT TEXT and the CUSTOM KNOWLEDGE BASE provided below. Prioritize information from the knowledge base if it's relevant.

                ---CUSTOM KNOWLEDGE BASE---
                {relevant_info}
                
                ---DOCUMENT TEXT---
                {document_text}

                ---QUESTION---
                {user_question}
                """
            # (Other analysis types remain the same)
            elif analysis_type == "📝 Concise Summary":
                final_prompt = f"Provide a concise, easy-to-read summary of the following document:\n\n{document_text}"
            elif analysis_type == "🔑 Key Topics":
                final_prompt = f"List the top 5-7 key topics or themes from the following document in a bulleted list:\n\n{document_text}"

            if final_prompt:
                st.info("Sending request to the AI model...")
                analysis_result = get_gemini_response(final_prompt)
                
                # --- START DEBUGGING ---
                if analysis_result is not None and analysis_result.strip():
                    st.success("Received a valid response from the AI!")
                    st.subheader("✨ Analysis Results")
                    st.markdown(analysis_result)
                elif analysis_result is not None:
                    st.error("🚨 The AI returned a blank response. This can happen due to safety filters or the content of the PDF. Please try a different PDF.")
                else:
                    # This happens if get_gemini_response returned None due to an exception
                    st.error("🚨 Failed to get a response from the AI model. Please check the error message above.")
                # --- END DEBUGGING ---

else:
    st.info("Please upload a document and select an analysis option from the sidebar.")
