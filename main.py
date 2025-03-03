import streamlit as st
from src.config.constants import Constants
from src.graphs.workflow_graph import build_workflow


def run_workflow(prompt: str):
    """Run the software life cycle workflow and return results."""
    workflow = build_workflow()
    workflow.invoke({ "prompt": prompt })
    pass


if __name__ == "__main__":
    # Setup streamlit app
    st.title("Software Life Cycle Workflow")
    input_prompt = st.text_area(
        "Enter your input requirements:", placeholder=Constants.INPUT_PLACEHOLDER
    )

    if st.button("Generate"):
        if input_prompt:
            run_workflow(input_prompt)
        else:
            st.warning("Please enter your requirement!")
