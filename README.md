<<<<<<< HEAD
# Sensitive Data Detection & Compliance Assistant

This is an AI-powered Streamlit application that analyzes uploaded documents (PDF, TXT, CSV) to detect sensitive and confidential information, classify risks, generate compliance summaries, and allow users to query the document using natural language.

## Features
1. **Document Upload**: Supports PDF, TXT, and CSV file formats.
2. **Sensitive Data Detection**: Uses Regex to detect Aadhaar, PAN, Emails, Phones, Credit Cards, Bank Accounts (IFSC), Passwords/API Keys, and Employee IDs.
3. **Data Masking**: Provides an option to redact detected sensitive data.
4. **Risk Classification & Compliance Summary**: Leverages Gemini AI to classify document risk (Low, Medium, High) and provide compliance observations/remediation steps.
5. **Question Answering**: Uses Gemini AI to let users chat with their document.

## Setup Instructions 

### Prerequisites
*   Python 3.8+
*   A Google Gemini API Key. (Get one from [Google AI Studio](https://aistudio.google.com/))

### Installation
1. Clone the repository:
   ```bash
   git clone [Your_Repository_Link]
   cd [Your_Repository_Name]
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Environment Variables:
   Rename `.env.example` to `.env` and add your Gemini API key:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. Run the Streamlit Application:
   ```bash
   streamlit run app.py
   ```

## Architecture Overview 

The application follows a simple, monolithic architecture built on Streamlit:
*   **Frontend (UI)**: Built with `streamlit`, providing an interactive interface for file uploads, displaying results, and chatting.
*   **Text Processing Engine**: 
    *   `PyPDF2` for parsing PDFs.
    *   `pandas` for handling CSV structures.
    *   Native python string manipulation for TXT.
*   **Detection Engine**: Python `re` module (Regular Expressions) to find PII (Personally Identifiable Information) and other confidential strings.
*   **AI Engine**: Integrates with `google-generativeai` (Gemini-1.5-flash) via API to process the document text alongside structured prompts for summarization and Q&A.

## AI/ML Approach Used 

The project uses a hybrid approach for efficiency and accuracy:
1.  **Rule-based Matching (Regex)**: For highly structured and standardized data (like Aadhaar numbers, PAN cards, Emails, Credit Cards), Regular Expressions provide the fastest and most accurate deterministic approach without the token cost or latency of an LLM.
2.  **Generative AI (LLMs)**: For complex, context-dependent tasks like risk classification, generating comprehensive compliance summaries, and natural language Q&A, the application utilizes the **Google Gemini 1.5 Flash** model. We use prompt engineering to instruct the model to act as a compliance expert. The document text is injected directly into the prompt context (context window permitting) to ground the model's responses.

## Challenges Faced 

*   **Context Window Limits**: Extremely large PDFs or CSVs might exceed the context window token limits of the LLM. The current implementation truncates very large text to the first 10,000 characters as a basic mitigation, which might miss data at the end of large files.
*   **Regex Limitations**: While Regex is fast, it can produce false positives (e.g., a 10-digit part number being flagged as a phone number) or false negatives for poorly formatted text.
*   **File Parsing**: Extracting clean, readable text from complex PDFs (e.g., those with tables, images, or non-standard encodings) is challenging using simple libraries like `PyPDF2`.

## Future Improvements 

*   **RAG Implementation (Retrieval-Augmented Generation)**: Integrate ChromaDB or FAISS to chunk and vectorize large documents. This would solve the context window limit and improve Q&A accuracy for massive files.
*   **OCR Support**: Integrate `pytesseract` or similar libraries to extract text from scanned PDFs and images.
*   **Advanced NLP for Detection**: Replace or augment Regex with Named Entity Recognition (NER) models (like `spaCy` or `Transformers`) to detect context-sensitive entities (e.g., distinguishing a person's name from a street name).
*   **Multi-Document Support**: Allow users to upload a batch of documents and perform cross-document risk analysis.
*   **Authentication & Audit Logging**: Add user login and tracking to see who uploaded what document and what risks were identified, storing this in a database for compliance tracking.
=======
# Sensitive-Data-Detection-Compliance-Assistant
>>>>>>> 590da4b4639ff3c0347061185bbe4374d657df1a
