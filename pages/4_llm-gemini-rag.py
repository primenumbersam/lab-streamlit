import streamlit as st
import google.generativeai as genai
import PyPDF2
import io

st.title("📝 File Q&A with Gemini")
st.markdown("""
Upload a document (PDF, TXT, or MD) and ask questions about its content. 
This demo uses **Google Gemini** for reasoning.
""")

with st.sidebar:
    gemini_api_key = st.text_input("Gemini API Key", key="gemini_api_key", type="password", help="Get yours at https://aistudio.google.com/app/apikey")
    "[Get Google AI Studio API Key](https://aistudio.google.com/app/apikey)"

uploaded_file = st.file_uploader("Upload an article or document", type=("txt", "md", "pdf"))
question = st.text_input(
    "Ask something about the document",
    placeholder="Can you give me a short summary or extract key points?",
    disabled=not uploaded_file,
)

def extract_text(file):
    if file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    else:
        return file.read().decode()

if uploaded_file and question:
    if not gemini_api_key:
        st.info("Please add your Gemini API key in the sidebar to continue.")
    else:
        try:
            # Configure Gemini
            genai.configure(api_key=gemini_api_key)
            # Using latest Flash Lite for best efficiency and low latency
            model = genai.GenerativeModel('gemini-3.1-flash-lite-preview')
            
            # Extract text
            with st.spinner("Extracting text and thinking..."):
                content = extract_text(uploaded_file)
                
                # Construct prompt
                full_prompt = f"""
                Here is a document:
                ---
                {content}
                ---
                Question: {question}
                
                Please answer the question based on the document provided.
                """
                
                # Call Gemini
                response = model.generate_content(full_prompt)
                
                st.subheader("Answer")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"An error occurred: {e}")

st.divider()
st.info("Note: Large documents might exceed context limits. This is a basic RAG-style demo using prompt-stuffing.")
