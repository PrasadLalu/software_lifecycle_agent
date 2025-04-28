# import streamlit as st
# from dotenv import load_dotenv
# from langchain_groq import ChatGroq
# from typing import Literal
# from pydantic import BaseModel, Field
# from typing_extensions import TypedDict
# from langgraph.graph import StateGraph, START, END

# # Load environment variables
# load_dotenv()

# # Initialize LLaMA3 model
# llm = ChatGroq(model="llama3-70b-8192")

# # Define the graph state
# class State(TypedDict):
#     joke: str
#     topic: str
#     feedback: str


# # Function to generate a joke
# def llm_call_generator(state: State):
#     """LLM generates a joke"""
#     if state.get("feedback"):
#         msg = llm.invoke(f"Write a joke about {state['topic']} but take into account the feedback: {state['feedback']}")
#     else:
#         msg = llm.invoke(f"Write a joke about {state['topic']}")
#     return {"joke": msg.content}


# # Build the workflow
# optimizer_builder = StateGraph(State)

# # Add nodes
# optimizer_builder.add_node("llm_call_generator", llm_call_generator)

# # Connect nodes
# optimizer_builder.add_edge(START, "llm_call_generator")
# optimizer_builder.add_edge("llm_call_generator", END)

# # Compile the workflow
# optimizer_workflow = optimizer_builder.compile()

# # Streamlit UI
# st.title("AI Joke Generator 🤖😂")

# # Session state to store joke & feedback
# if "topic" not in st.session_state:
#     st.session_state.topic = ""
# if "joke" not in st.session_state:
#     st.session_state.joke = ""
# if "feedback" not in st.session_state:
#     st.session_state.feedback = ""

# # User input for topic
# topic = st.text_input("Enter a topic for the joke:", st.session_state.topic)

# if st.button("Generate Joke"):
#     if topic:
#         # Invoke the workflow with the user input
#         state = optimizer_workflow.invoke({"topic": topic})
#         st.session_state.joke = state["joke"]
#         st.session_state.topic = topic
#         st.session_state.feedback = ""  # Reset feedback
#         st.rerun()
#     else:
#         st.warning("Please enter a topic before generating a joke!")

# # Display the joke if available
# if st.session_state.joke:
#     st.subheader("Here's your joke:")
#     st.write(st.session_state.joke)

#     # User feedback buttons
#     col1, col2 = st.columns(2)
#     with col1:
#         if st.button("😂 Accepted"):
#             st.success("Glad you liked it! 🎉")
#             st.session_state.joke = ""  # Clear joke to reset for a new one
#             st.session_state.topic = ""  # Reset topic input
#             st.rerun()

#     with col2:
#         if st.button("😐 Rejected"):
#             feedback = st.text_input("What could be improved?", key="feedback_input")
#             if feedback and st.button("Submit Feedback"):
#                 # Generate a new joke with feedback
#                 print(feedback)
#                 state = optimizer_workflow.invoke({"topic": feedback})
#                 st.session_state.joke = state["joke"]
#                 st.write(st.session_state.joke)
#                 st.rerun()


import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

# Load environment variables
load_dotenv()

# Initialize LLaMA3 model
llm = ChatGroq(model="llama3-70b-8192")

# Define the graph state
class State(TypedDict):
    joke: str
    topic: str
    feedback: str


# Function to generate a joke
def llm_call_generator(state: State):
    """LLM generates a joke"""
    if state.get("feedback"):
        msg = llm.invoke(f"Write a joke about {state['topic']} but take into account the feedback: {state['feedback']}")
    else:
        msg = llm.invoke(f"Write a joke about {state['topic']}")
    return {"joke": msg.content}


# Build the workflow
optimizer_builder = StateGraph(State)
optimizer_builder.add_node("llm_call_generator", llm_call_generator)
optimizer_builder.add_edge(START, "llm_call_generator")
optimizer_builder.add_edge("llm_call_generator", END)
optimizer_workflow = optimizer_builder.compile()

# Streamlit UI
st.title("AI Joke Generator 🤖😂")

# Initialize session state variables
if "topic" not in st.session_state:
    st.session_state.topic = ""
if "joke" not in st.session_state:
    st.session_state.joke = ""
if "feedback" not in st.session_state:
    st.session_state.feedback = ""
if "show_feedback_input" not in st.session_state:
    st.session_state.show_feedback_input = False  # Controls feedback input visibility

# User input for topic
topic = st.text_input("Enter a topic for the joke:", st.session_state.topic)

if st.button("Generate Joke"):
    if topic:
        state = optimizer_workflow.invoke({"topic": topic})
        st.session_state.joke = state["joke"]
        st.session_state.topic = topic
        st.session_state.feedback = ""  # Reset feedback
        st.session_state.show_feedback_input = False  # Hide feedback input
        st.rerun()
    else:
        st.warning("Please enter a topic before generating a joke!")

# Display the joke if available
if st.session_state.joke:
    st.subheader("Here's your joke:")
    st.write(st.session_state.joke)

    # User feedback buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("😂 Accepted"):
            st.success("Glad you liked it! 🎉")
            st.session_state.joke = ""
            st.session_state.topic = ""
            st.session_state.show_feedback_input = False
            st.rerun()

    with col2:
        if st.button("😐 Rejected"):
            st.session_state.show_feedback_input = True
            st.rerun()

# Show feedback input if "Rejected" was clicked
if st.session_state.show_feedback_input:
    st.session_state.feedback = st.text_input("What could be improved?", st.session_state.feedback)

    if st.button("Submit Feedback"):
        if st.session_state.feedback:
            state = optimizer_workflow.invoke(
                # {"topic": st.session_state.topic, "feedback": st.session_state.feedback}
                {"topic": st.session_state.feedback}
            )
            st.session_state.joke = state["joke"]
            st.session_state.show_feedback_input = False  # Hide input after submission
            st.rerun()
        else:
            st.warning("Please provide feedback before submitting!")
