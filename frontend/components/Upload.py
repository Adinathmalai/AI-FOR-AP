import streamlit as st
import pandas as pd
import pdfplumber
import docx
from io import BytesIO
import os

def get_mime_type(uploaded_file):
    ext = uploaded_file.name.split('.')[-1].lower()
    mime_map = {
        'pdf': 'application/pdf',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'xls': 'application/vnd.ms-excel',
        'csv': 'text/csv',
        'txt': 'text/plain'
    }
    return mime_map.get(ext, 'application/octet-stream')

def clean_text(text):
    return ' '.join(text.split()).strip()

def dataframe_to_text(df):
    # Convert DataFrame to clean line-by-line text
    text = ""
    for _, row in df.iterrows():
        line = ', '.join(f"{col}: {row[col]}" for col in df.columns if pd.notnull(row[col]))
        text += line + "\n"
    return text.strip()

def upload_and_parse():
    uploaded_files = st.file_uploader(
        "📁 Upload CDR / IPDR / FIR Files",
        type=['csv', 'xlsx', 'xls', 'pdf', 'docx', 'txt'],
        accept_multiple_files=True,
        key="multi_file_uploader"
    )

    if not uploaded_files:
        return None

    full_text = ""
    parsed_data = []

    for uploaded_file in uploaded_files:
        try:
            file_type = get_mime_type(uploaded_file)
            file_name = uploaded_file.name

            file_info = {
                "name": file_name,
                "type": file_type,
                "size": f"{len(uploaded_file.getvalue()) / 1024:.2f} KB",
            }

            # Process various file types
            if file_type == "application/pdf":
                with pdfplumber.open(uploaded_file) as pdf:
                    pages = [clean_text(page.extract_text()) for page in pdf.pages if page.extract_text()]
                    text = "\n".join(pages)

            elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                doc = docx.Document(BytesIO(uploaded_file.read()))
                text = clean_text("\n".join(para.text for para in doc.paragraphs if para.text))

            elif file_type in ["application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
                df = pd.read_excel(uploaded_file)
                text = clean_text(dataframe_to_text(df))

            elif file_type == "text/csv":
                df = pd.read_csv(uploaded_file)
                text = clean_text(dataframe_to_text(df))

            elif file_type == "text/plain":
                text = uploaded_file.read().decode("utf-8", errors="ignore")
                text = clean_text(text)

            else:
                st.warning(f"⚠️ Unsupported file type: {file_name}")
                continue

            full_text += f"\n\n---\n\nFile: {file_name}\n\n{text}"
            file_info["content"] = text
            parsed_data.append(file_info)
            st.success(f"✅ Processed: {file_name}")

        except Exception as e:
            st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")

    return full_text if full_text.strip() else None
