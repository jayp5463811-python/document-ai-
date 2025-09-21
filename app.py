import google.generativeai as genai
from pdf2image import convert_from_path
import base64
import io
import os
from dotenv import load_dotenv

# --- IMPORTANT: CONFIGURE YOUR API KEY ---
# For security, it's best to load your key from a .env file.
# 1. Create a file named .env in the same folder.
# 2. In that file, write: GOOGLE_API_KEY="YOUR_KEY_HERE"
# 3. This code will then load it securely.
load_dotenv()
API_KEY = os.getenv("AIzaSyAjk_X7L9LWPEHvxQ7rVkEq4rylABuuAng")

# If you don't use a .env file, you can uncomment the line below,
# but DO NOT save your real key to GitHub.
# API_KEY = "YOUR_GOOGLE_API_KEY"

if not API_KEY:
    raise ValueError("API Key not found. Please set it in a .env file or directly in the code.")

genai.configure(api_key=API_KEY)


def prepare_document_for_gemini(file_path, mime_type):
    """
    Converts a file (PDF or image) into a list of parts for the Gemini API.
    """
    # 1. Handle PDF: Convert pages to images
    if mime_type == 'application/pdf':
        images = convert_from_path(file_path)
        parts = []
        for image in images:
            # Convert PIL image to bytes
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

    # 2. Handle Images
    elif mime_type.startswith('image/'):
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

    try:
        print(f"Preparing document: {file_path}...")
        document_parts = prepare_document_for_gemini(file_path, mime_type)

        print("Calling Gemini API...")
        model = genai.GenerativeModel('gemini-1.5-flash') # Use a model that supports images

        # The prompt must be the first part, followed by the document parts
        full_prompt = [prompt] + document_parts

        response = model.generate_content(full_prompt)
        return response.text

    except Exception as e:
        print(f"An error occurred: {e}")
        return f"Error processing the document: {str(e)}"

# --- HOW TO RUN THIS SCRIPT ---
# 1. Make sure you have a test file (e.g., 'my_document.pdf' or 'my_image.png') in the same folder.
# 2. Change the file_path and prompt variables below.
# 3. Run the script from your terminal: python app.py
if __name__ == '__main__':
    # --- EDIT THESE VALUES FOR YOUR TEST ---
    file_to_analyze = "test.pdf" # IMPORTANT: Change this to your file's name
    mime_type_of_file = "application/pdf" # Change to "image/png" or "image/jpeg" if it's an image
    your_prompt = "Summarize this document in three bullet points."
    # -----------------------------------------

    print("--- Starting Document Analysis ---")
    result = ask_gemini_about_document(
        prompt=your_prompt,
        file_path=file_to_analyze,
        mime_type=mime_type_of_file
    )
    print("\n--- Gemini Response ---")
    print(result)
    print("-------------------------")

