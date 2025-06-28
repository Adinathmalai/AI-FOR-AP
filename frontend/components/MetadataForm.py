import streamlit as st

def metadata_form():
    st.subheader("Metadata Form")
    name = st.text_input("Dataset Name")
    doc_type = st.selectbox("Document Type", ["CDR", "IPDR", "FIR", "Summary", "Others"])
    definition = st.text_area("Definition")
    intelligence_level = st.slider("Intelligence Level", 1, 10, 1)
    return {"name": name, "type": doc_type, "definition": definition, "level": intelligence_level}
