import google.generativeai as genai
import base64
import io
import os
from dotenv import load_dotenv

# --- Step 1: Try to import the PDF library ---
try:
    from pdf2image import convert_from_path
    PDF_LIBRARY_AVAILABLE = True
except ImportError:
    PDF_LIBRARY_AVAILABLE = False

print("--- Script Starting ---")

# --- Step 2: Configure API Key ---
print("-> Loading API Key...")
load_dotenv()
API_KEY = os.getenv("AIzaSyBxpRh79rp0ThZqkEaB4wSkBcOwT_JA4Ig")

if not API_KEY:
    print("❌ ERROR: API Key not found.")
    raise ValueError("Please set your GOOGLE_API_KEY in a .env file.")

genai.configure(api_key=API_KEY)
print("-> API Key configured successfully.")


def prepare_document_for_gemini(file_path, mime_type):
    """
    Converts a file (PDF or image) into a list of parts for the Gemini API.
    """
    print("-> Preparing document for Gemini...")
    # 1. Handle PDF: Convert pages to images
    if mime_type == 'application/pdf':
        if not PDF_LIBRARY_AVAILABLE:
            print("❌ ERROR: The 'pdf2image' library is not installed. Cannot process PDFs.")
            print("Please run: pip install pdf2image")
            return None
        try:
            print("-> Found a PDF. Attempting to convert pages to images...")
            images = convert_from_path(file_path)
            print(f"-> Successfully converted {len(images)} page(s).")
            parts = []
            for image in images:
                buffered = io.BytesIO()
                image.save(buffered, format="JPEG")
                img_byte = buffered.getvalue()
                parts.append({
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": base64.b64encode(img_byte).decode('utf-8')
                    }
                })
            return parts
        except Exception as e:
            # This is the most common error point for PDFs.
            print("\n--- ❌ PDF CONVERSION FAILED ---")
            print(f"Error details: {e}")
            print("\nThis error almost always means that 'Poppler', a required program for handling PDFs, is not installed or not in your system's PATH.")
            print("Please search online for 'how to install poppler on Windows/Mac/Linux' for instructions.")
            return None  # Return None to indicate failure

    # 2. Handle Images
    elif mime_type.startswith('image/'):
        print("-> Found an image. Reading file...")
        with open(file_path, "rb") as f:
            img_byte = f.read()
        return [{
            "inline_data": {
                "mime_type": mime_type,
                "data": base64.b64encode(img_byte).decode('utf-8')
            }
        }]
    else:
        raise ValueError("Unsupported file type. Please upload a PDF or an image.")

def ask_gemini_about_document(prompt, file_path, mime_type):
    """
    Main function to process a document and get a response from Gemini.
    """
    if not os.path.exists(file_path):
        return f"Error: The file '{file_path}' was not found."

    document_parts = prepare_document_for_gemini(file_path, mime_type)

    # Check if the preparation step failed (e.g., Poppler error)
    if document_parts is None:
        return "Document preparation failed. Please see the error message above."

    try:
        print("-> Calling Gemini API...")
        model = genai.GenerativeModel('gemini-1.5-flash')
        full_prompt = [prompt] + document_parts
        response = model.generate_content(full_prompt)
        print("-> Got a response from Gemini!")
        return response.text

    except Exception as e:
        return f"An error occurred with the Gemini API: {str(e)}"

# --- HOW TO RUN THIS SCRIPT ---
if __name__ == '__main__':
    # --- EDIT THESE VALUES FOR YOUR TEST ---
    file_to_analyze = "test.pdf" # IMPORTANT: Change this to your file's name
    mime_type_of_file = "application/pdf" # Change to "image/png" or "image/jpeg" if it's an image
    your_prompt = "Summarize this document in three bullet points."
    # -----------------------------------------

    print("\n--- Starting Document Analysis ---")
    result = ask_gemini_about_document(
        prompt=your_prompt,
        file_path=file_to_analyze,
        mime_type=mime_type_of_file
    )
    print("\n--- Gemini Response ---")
    print(result)
    print("-------------------------")

