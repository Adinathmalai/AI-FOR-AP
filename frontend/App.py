# App.py

import streamlit as st
from components.auth import login_ui
from components.Upload import upload_and_parse
from components.MetadataForm import metadata_form
from components.CopilotChat import copilot_chat
from components.GraphView import graph_view
from components.MapView import map_view
from components.Voiceinput import voice_input_handler
import sys
sys.path.insert(0, 'C:/Users/KEERTHANA S/Desktop/final project')

st.set_page_config(layout="wide")
st.title("🔍 CDR/IPDR Intelligence Copilot Engine")

# ✅ Login Authentication
if "user" not in st.session_state:
    if not login_ui():
        st.stop()

# ✅ Welcome Message
user_info = st.session_state['user']
st.success(f"Welcome, {user_info['email']} ({user_info['designation']})!")

# ✅ File Upload & Parsing
data = upload_and_parse()

# ✅ Handle Data If Uploaded
if data is not None:
    if isinstance(data, str):
        st.text_area("Extracted Text", value=data, height=300)
    else:
        st.dataframe(data)
        graph_view(data)
        map_view(data)

    # ✅ Metadata Editing
    meta = metadata_form()
    st.write("Metadata:", meta)

    # ✅ Voice Input from User
    query_text = voice_input_handler()  # Uses sounddevice to capture voice

    # ✅ Handle Copilot Chat
    if query_text:
        st.text_input("Recognized Voice Input", value=query_text)
        copilot_chat(data, initial_query=query_text)
    else:
        copilot_chat(data)
