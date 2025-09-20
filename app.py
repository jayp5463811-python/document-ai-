import google.generativeai as genai
from pdf2image import convert_from_path
import base64
import io

# --- CONFIGURE YOUR API KEY ---
# Best practice: Load from environment variables, not hardcoded
# from dotenv import load_dotenv
# import os
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key="YOUR_GOOGLE_API_KEY")


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
    try:
        print("Preparing document...")
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

# Example Usage (for testing)
# if __name__ == '__main__':
#     # Make sure you have a test file named 'test.pdf' or 'test.png'
#     result = ask_gemini_about_document(
#         prompt="Summarize this document in three bullet points.",
#         file_path="test.pdf",
#         mime_type="application/pdf"
#     )
#     print("\n--- Gemini Response ---")
#     print(result)
