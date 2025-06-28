# frontend/components/GraphView.py
import streamlit as st
import pandas as pd

def graph_view(data):
    """Universal data visualizer for any tabular data"""
    if not data:
        return
    
    if isinstance(data, list):
        for file in data:
            if 'content' in file and file['content']['type'] == 'dataframe':
                df = file['content']['data']
                try:
                    st.subheader(f"Analysis for {file['name']}")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        x_axis = st.selectbox("X-Axis", df.columns, key=f"x_{file['name']}")
                    
                    with col2:
                        y_axis = st.selectbox("Y-Axis", df.columns, key=f"y_{file['name']}")
                    
                    if st.button("Generate Graph", key=f"btn_{file['name']}"):
                        st.line_chart(df[[x_axis, y_axis]])
                except Exception as e:
                    st.error(f"Graph error in {file['name']}: {str(e)}")
    elif isinstance(data, pd.DataFrame):
        # Same for single DataFrame
        col1, col2 = st.columns(2)
        with col1:
            x_axis = st.selectbox("X-Axis", data.columns)
        with col2:
            y_axis = st.selectbox("Y-Axis", data.columns)
        if st.button("Generate Graph"):
            st.line_chart(data[[x_axis, y_axis]])
