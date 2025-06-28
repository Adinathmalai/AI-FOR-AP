import pandas as pd
import pdfplumber
import docx

def parse_file(uploaded_file, file_type):
    if file_type == "xlsx":
        return pd.read_excel(uploaded_file)
    elif file_type == "csv":
        return pd.read_csv(uploaded_file)
    elif file_type == "pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    elif file_type == "docx":
        doc = docx.Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs])
    return None
