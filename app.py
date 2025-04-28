# import streamlit as st
# from dotenv import load_dotenv
# from langchain_groq import ChatGroq
# from typing_extensions import TypedDict
# from langgraph.graph import StateGraph, START, END

# # Load env vars
# load_dotenv()

# # Initialize Llama model
# llm = ChatGroq(model="llama3-70b-8192")


# class State(TypedDict):
#     prompt: str
#     content: str
#     documents: str
#     codes: str
#     user_review_status: str


# # Nodes
# def get_user_requirement(state: State):
#     """Act as a senior data scientist. Please give answer based on your ability."""
#     result = llm.invoke(f"Give me the answer for the query: {state['prompt']}")
#     return {"content": result.content}


# def review_by_user(state: State):
#     user_review_status = st.selectbox("Review Status", ["accepted", "feedback"])
#     return {"user_review_status": user_review_status}


# def create_design_document(state: State):
#     return {"documents": "Document created."}


# def generate_code(state: State):
#     return {"codes": "Code generated."}


# def route_user_review(state: State):
#     if state["user_review_status"] == "accepted":
#         return "Accepted"
#     elif state["user_review_status"] == "feedback":
#         return "Feedback"


# # Build Workflow
# workflow_builder = StateGraph(State)

# # Add nodes
# workflow_builder.add_node("user_requirement", get_user_requirement)
# workflow_builder.add_node("user_review", review_by_user)
# workflow_builder.add_node("design_document", create_design_document)
# workflow_builder.add_node("generate_code", generate_code)


# # Add edges to connect nodes
# workflow_builder.add_edge(START, "user_requirement")
# workflow_builder.add_edge("user_requirement", "user_review")
# workflow_builder.add_conditional_edges(
#     "user_review",
#     route_user_review,
#     {
#         "Accepted": "generate_code",
#         "Feedback": "design_document",
#     },
# )
# workflow_builder.add_edge("generate_code", END)

# st.title("AI Agent Automation")
# input_query = st.text_input("Enter your query")

# if st.button("Generate"):
#     if input_query:
#         workflow = workflow_builder.compile()
#         result = workflow.invoke({"prompt": input_query})
#         st.write(result["content"])
#     else:
#         st.warning("Please enter your query!")


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


# Nodes
def get_user_requirement(state: State):
    """Act as a senior data scientist. Please give an answer based on your ability."""
    result = llm.invoke(f"Give me the answer for the query: {state['prompt']}")
    return {"content": result.content}  # Merge with existing state


def review_by_user(state: State):
    st.write("Review the generated response:")
    st.write(state["content"])  # Display generated content
    user_review_status = st.radio("Review Status", ["accepted", "feedback"])
    return {"user_review_status": user_review_status}  # Merge state


def create_design_document(state: State):
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

# Add nodes
workflow_builder.add_node("user_requirement", get_user_requirement)
workflow_builder.add_node("user_review", review_by_user)
workflow_builder.add_node("design_document", create_design_document)
workflow_builder.add_node("generate_code", generate_code)


# Add edges to connect nodes
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

st.title("AI Agent Automation")
input_query = st.text_input("Enter your query")

if st.button("Generate"):
    if input_query:
        workflow = workflow_builder.compile()

        # Initialize the workflow with default values
        result = workflow.invoke({"prompt": input_query})

        # Display the results
        st.subheader("Final Output:")
        st.write("Answer:", result.get("content", ""))
        st.write("Document:", result.get("documents", ""))
        st.write("Code:", result.get("codes", ""))
    else:
        st.warning("Please enter your query!")
