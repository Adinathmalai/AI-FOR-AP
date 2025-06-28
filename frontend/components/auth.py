import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st
# from backend.supabase.auth import login_user  # No longer needed

def login_ui():
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    designation = st.text_input("Designation ID")

    if st.button("Login"):
      
        user = {
            "email": email,
            "designation": designation
        }
        st.success("Login successful (authentication bypassed)")
        st.session_state['user'] = user
        return True
    return False
