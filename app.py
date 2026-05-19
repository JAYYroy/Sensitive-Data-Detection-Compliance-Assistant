import streamlit as st
import os
from dotenv import load_dotenv
from utils import (
    extract_text_from_file, 
    detect_sensitive_data, 
    mask_sensitive_data, 
    analyze_document_with_ai, 
    answer_question_with_ai,
    setup_gemini
)

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="Sensitive Data Detection & Compliance Assistant", layout="wide")

def main():
    st.title("🛡️ Sensitive Data Detection & Compliance Assistant")
    st.markdown("Upload a document (PDF, TXT, CSV) to detect sensitive information, classify risks, and generate compliance summaries.")

    if not API_KEY or API_KEY == "your_gemini_api_key_here":
        st.warning("⚠️ Please add your Gemini API Key to the .env file to enable AI features (Summary and Q&A).")
    else:
        setup_gemini(API_KEY)

    # Sidebar for upload
    with st.sidebar:
        st.header("1. Upload Document")
        uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt", "csv"])

    if uploaded_file is not None:
        with st.spinner("Extracting text..."):
            try:
                raw_text = extract_text_from_file(uploaded_file)
            except Exception as e:
                st.error(f"Error reading file: {e}")
                return

        if not raw_text.strip():
            st.warning("The uploaded document is empty or text could not be extracted.")
            return

        # --- Step 2: Sensitive Data Detection ---
        st.header("🔍 2. Sensitive Data Detection")
        with st.spinner("Scanning for sensitive data..."):
            detected_data = detect_sensitive_data(raw_text)

        if detected_data:
            st.error("⚠️ Sensitive Information Detected!")
            
            # Display detected data in expanders
            for label, items in detected_data.items():
                with st.expander(f"{label} ({len(items)} found)"):
                    for item in items:
                        st.write(f"- `{item}`")
            
            # Show Data Masking option
            if st.checkbox("Show Masked Document"):
                st.subheader("Masked Content Preview")
                masked_text = mask_sensitive_data(raw_text, detected_data)
                st.text_area("Masked Text", masked_text, height=300)
        else:
            st.success("✅ No standard sensitive information (Regex) detected.")


        # --- Step 3 & 4: Risk Classification & AI Summary ---
        st.header("📊 3. Risk Classification & Compliance Summary")
        if st.button("Generate AI Summary"):
            if not API_KEY or API_KEY == "your_gemini_api_key_here":
                st.error("Gemini API Key is missing. Cannot generate AI Summary.")
            else:
                with st.spinner("Analyzing document with AI..."):
                    ai_summary = analyze_document_with_ai(raw_text)
                    st.markdown(ai_summary)

        # --- Step 5: Question Answering ---
        st.header("💬 4. Ask Questions")
        st.markdown("Ask anything about the uploaded document.")
        user_question = st.text_input("Enter your question:")
        
        if st.button("Ask"):
            if not user_question:
                st.warning("Please enter a question.")
            elif not API_KEY or API_KEY == "your_gemini_api_key_here":
                st.error("Gemini API Key is missing. Cannot use Q&A.")
            else:
                with st.spinner("Finding answer..."):
                    answer = answer_question_with_ai(raw_text, user_question)
                    st.info(answer)

if __name__ == "__main__":
    main()
