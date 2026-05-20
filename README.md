Sensitive Data Detection & Compliance Assistant
A Streamlit-based web app that scans uploaded documents for sensitive information, classifies risk levels, and lets you ask questions about the document using AI.
Built this as part of an internship assignment. The idea was to combine regex-based detection for structured data (like Aadhaar, PAN) with an LLM for the more contextual stuff like risk summaries and Q&A.
Live Demo: https://sensitive-data-detection-compliance-assistant-nj6uszmnushegfiw.streamlit.app
GitHub: https://github.com/JAYYroy/Sensitive-Data-Detection-Compliance-Assistant


What it does

Upload a PDF, TXT, or CSV file
Automatically detects sensitive data like Aadhaar numbers, PAN cards, emails, phone numbers, credit cards, bank details, API keys, and employee IDs
Option to view a masked version of the document where sensitive values are redacted
Click "Generate AI Summary" to get a risk classification (Low / Medium / High) and a compliance summary powered by Gemini
Ask any question about the document in plain English and get an answer


Setup Instructions
Requirements

Python 3.8+
A Gemini API key from Google AI Studio

Install dependencies
pip install -r requirements.txt
Add your API key
Rename .env.example to .env and paste your key:
GEMINI_API_KEY=your_key_here
Run the app
streamlit run app.py
Streamlit Cloud Deployment

Push code to GitHub
Connect repo on share.streamlit.io
Add GEMINI_API_KEY under Settings > Secrets
App deploys automatically on every commit


Architecture Overview
The app follows a simple modular structure built on Streamlit:
User uploads file (PDF / TXT / CSV)
        |
        v
Text Extraction Layer
  - PyPDF2 for PDFs
  - pandas for CSVs
  - native Python for TXT
        |
        v
Detection Engine
  - Python re module (Regex)
  - Scans for PII patterns
        |
        v
AI Engine (Google Gemini 2.5 Flash)
  - Risk classification
  - Compliance summary
  - Q&A over document
        |
        v
Streamlit UI
  - Displays results, masked text, AI output

File structure:
app.py              # Streamlit UI and application flow
utils.py            # Core logic: extraction, detection, masking, AI calls
requirements.txt    # Python dependencies
.env.example        # API key template
.gitignore          # Excludes .env and secrets from version control

AI/ML Approach
Detection is split into two parts depending on what we are looking for.
For structured data like Aadhaar numbers, PAN cards, and credit cards, regex is the right tool. It is fast, does not need an API call, and works reliably for patterns that follow a fixed format.
For everything else — risk classification, compliance observations, and answering questions — the app uses Google Gemini 2.5 Flash. The document text gets injected into a prompt along with instructions telling the model to behave like a security and compliance expert. For Q&A, the model is explicitly told to only use the document content so it does not hallucinate.
The Gemini API is called directly via HTTP requests to the v1beta endpoint rather than through the SDK, which had version compatibility issues during development.
Hybrid approach summary:

Regex — fast, deterministic, no API cost, best for fixed patterns
Gemini LLM — context-aware, handles complex analysis and natural language


Challenges Faced
A few things took longer than expected:

Model deprecation — Started with gemini-1.5-flash which returned a 404. Switched to gemini-2.0-flash which had zero free quota. Finally got it working with gemini-2.5-flash on the v1beta endpoint.
SDK version conflict — The google-generativeai library was using an outdated internal API version. Ended up bypassing it entirely and making direct HTTP calls using Python's requests library instead.
Regex false positives — Generic 10-digit numbers sometimes match phone number patterns. It is a known tradeoff with regex-only detection.
PDF parsing — PyPDF2 works fine for standard text-based PDFs but struggles with scanned or image-heavy documents.
Context window limits — Very large documents exceed the LLM token limit. Currently mitigated by truncating to the first 10,000 characters.


Future Improvements

RAG with ChromaDB or FAISS — Right now large documents get truncated at 10,000 characters. A proper chunking and retrieval setup would fix this and improve Q&A accuracy on large files.
OCR support — pytesseract integration for scanned PDFs and image-based documents
Better NLP detection — spaCy or a HuggingFace NER model would catch context-sensitive entities that regex misses
Audit logging — Track who uploaded what and what was flagged, stored in a database for compliance tracking
Multi-document support — Compare risk across a batch of uploaded files
Export reports — Let users download the compliance summary as a PDF
Dockerization — Package the app for consistent, environment-independent deployment


Tech Stack

Python, Streamlit
PyPDF2, pandas
Google Gemini 2.5 Flash (direct REST API, v1beta)
Python re module (Regex)
