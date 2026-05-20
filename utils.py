import re
import os
import PyPDF2
import pandas as pd
import requests
from io import StringIO, BytesIO

# Regex patterns for Sensitive Data Detection
PATTERNS = {
    "Aadhaar Number": r"\b\d{4}\s\d{4}\s\d{4}\b|\b\d{12}\b",
    "PAN Number": r"\b[A-Z]{5}\d{4}[A-Z]{1}\b",
    "Email Address": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b",
    "Phone Number": r"\b(?:\+?91[\-\s]?)?[6789]\d{9}\b|\b\d{10}\b",
    "Credit Card Number": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
    "Bank Account / IFSC": r"\b[A-Z]{4}0[A-Z0-9]{6}\b|\b\d{9,18}\b",
    "API Key / Password": r"(?i)(?:api_key|apikey|password|secret|token)[\s:=]+[\"']?([a-zA-Z0-9\-_]{8,})[\"']?",
    "Employee ID": r"\b(?:EMP|ID)[-\s]?\d{3,6}\b"
}

def setup_gemini(api_key):
    """Initializes Gemini API."""
    os.environ["GEMINI_API_KEY"] = api_key

def get_gemini_model():
    return None

def extract_text_from_file(uploaded_file):
    """Extracts text from uploaded PDF, TXT, or CSV file."""
    if uploaded_file is None:
        return ""
    
    file_type = uploaded_file.name.split('.')[-1].lower()
    text = ""
    
    if file_type == 'pdf':
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
    elif file_type == 'txt':
        text = uploaded_file.getvalue().decode("utf-8")
    elif file_type == 'csv':
        df = pd.read_csv(uploaded_file)
        text = df.to_string()
    else:
        raise ValueError("Unsupported file type")
        
    return text

def detect_sensitive_data(text):
    """Detects sensitive data using Regex."""
    detected_data = {}
    for label, pattern in PATTERNS.items():
        matches = re.finditer(pattern, text)
        found = [match.group() for match in matches]
        if found:
            detected_data[label] = list(dict.fromkeys(found))
            
    return detected_data

def mask_sensitive_data(text, detected_data):
    """Masks detected sensitive data in the text."""
    masked_text = text
    for label, items in detected_data.items():
        for item in items:
            if len(item) > 4:
                masked = '*' * (len(item) - 4) + item[-4:]
            else:
                masked = '*' * len(item)
            masked_text = masked_text.replace(item, f"[{label}: {masked}]")
    return masked_text

def call_gemini_api(prompt):
    """Calls Gemini API directly using REST."""
    api_key = os.environ.get("GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    try:
        response = requests.post(url, json=data)
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Error: {str(e)} - Response: {response.text}"

def analyze_document_with_ai(text):
    """Uses Gemini API to analyze document risk and generate a summary."""
    prompt = f"""
    You are a Security and Compliance Expert.
    Analyze the following document content and provide:
    1. Risk Classification (Low Risk, Medium Risk, or High Risk) based on the presence of sensitive personal or corporate data.
    2. A Compliance & Security Summary, including:
       - Compliance observations (e.g., GDPR, DPDPA implications if PII is present).
       - Security risks.
       - Suggested remediation steps.

    Format the response cleanly in Markdown. Do NOT quote the sensitive data directly in your response.

    Document Content:
    {text[:10000]}
    """
    return call_gemini_api(prompt)

def answer_question_with_ai(text, question):
    """Answers user questions about the document."""
    prompt = f"""
    You are an AI assistant helping a user understand a document.
    Answer the following question based ONLY on the provided document content.
    If the answer is not in the document, say "I cannot find the answer in the document."

    Question: {question}

    Document Content:
    {text[:10000]}
    """
    return call_gemini_api(prompt)
