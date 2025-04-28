import streamlit as st
from src.config.constants import Constants


def create_ui():
    # Setup streamlit app
    st.title("Software Life Cycle Workflow")
    input_prompt = st.text_area(
        "Enter your input requirements:", placeholder=Constants.INPUT_PLACEHOLDER
    )

    if st.button("Generate"):
        if input_prompt:
            return input_prompt
        else:
            st.warning("Please enter your requirement!")
