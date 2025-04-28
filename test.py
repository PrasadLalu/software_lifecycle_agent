import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

# Load env vars
load_dotenv()

# Initialize Llama model
llm = ChatGroq(model="llama3-70b-8192")


class State(TypedDict):
    prompt: str
    content: str
    documents: str
    codes: str
    user_review_status: str
    user_feedback: str


# Initialize session state
if "content" not in st.session_state:
    st.session_state.content = ""
if "user_review_status" not in st.session_state:
    st.session_state.user_review_status = None
if "user_feedback" not in st.session_state:
    st.session_state.user_feedback = ""


# Nodes
def get_user_requirement(state: State):
    result = llm.invoke(
        f"Give me the answer in 300 characters for the query: {state['prompt']}"
    )
    st.session_state.content = result.content
    return {"content": result.content}


def review_by_user(state: State):
    if st.session_state.user_review_status is None:
        st.session_state.user_review_status = "feedback"

    with st.form(key="review_form"):
        st.write("Review the generated response:")
        st.write(st.session_state.content)

        user_review_status = st.radio(
            "Enter review status (Accepted/Feedback):",
            ["accepted", "feedback"],
            index=0 if st.session_state.user_review_status == "accepted" else 1,
            key="review_status_form",
        )

        user_feedback = st.session_state.user_feedback
        if user_review_status == "feedback":
            user_feedback = st.text_area(
                "Provide feedback details:",
                value=st.session_state.user_feedback,
                placeholder="Enter your suggestions or modifications needed...",
                key="feedback_input_form",
            )

        if st.form_submit_button("Submit Review"):
            st.session_state.user_review_status = user_review_status
            st.session_state.user_feedback = (
                user_feedback if user_review_status == "feedback" else ""
            )
            st.rerun() #add this line

        return {
            "user_review_status": st.session_state.user_review_status,
            "user_feedback": st.session_state.user_feedback,
        }


def create_design_document(state: State):
    if state["user_feedback"]:
        return {
            "documents": f"Document created based on feedback: {st.session_state.user_feedback}"
        }
    else:
        st.session_state.documents = "Document created."
    return {"documents": "Document created."}


def generate_code(state: State):
    return {"codes": "Code generated."}


def route_user_review(state: State):
    if state["user_review_status"] == "accepted":
        return "Accepted"
    elif state["user_review_status"] == "feedback":
        return "Feedback"


# Build Workflow
workflow_builder = StateGraph(State)
workflow_builder.add_node("user_requirement", get_user_requirement)
workflow_builder.add_node("user_review", review_by_user)
workflow_builder.add_node("design_document", create_design_document)
workflow_builder.add_node("generate_code", generate_code)

workflow_builder.add_edge(START, "user_requirement")
workflow_builder.add_edge("user_requirement", "user_review")
workflow_builder.add_conditional_edges(
    "user_review",
    route_user_review,
    {
        "Accepted": "generate_code",
        "Feedback": "design_document",
    },
)
workflow_builder.add_edge("generate_code", END)

# Main app
st.title("AI Agent Automation")
input_query = st.text_input("Enter your query")

if st.button("Generate"):
    if input_query:
        workflow = workflow_builder.compile()
        initial_state = {"prompt": input_query}
        result = workflow.invoke(initial_state)
        print(result)
    else:
        st.warning("Please enter your query!")


# # Display review status, feedback, documents, and codes
# if st.session_state.user_review_status:
#     st.write("Review Status:", st.session_state.user_review_status)
#     if (
#         st.session_state.user_review_status == "feedback"
#         and st.session_state.user_feedback
#     ):
#         st.write("User Feedback:")
#         st.write(st.session_state.user_feedback)

if st.session_state.documents:
    st.write("Design Document:")
    st.write(st.session_state.documents)

# if st.session_state.codes:
#     st.write("Generated Code:")
#     st.write(st.session_state.codes)
