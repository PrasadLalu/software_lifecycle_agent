# import streamlit as st
# from dotenv import load_dotenv
# from langchain_groq import ChatGroq
# from typing_extensions import TypedDict
# from langgraph.graph import StateGraph, START, END

# # Load environment variables
# load_dotenv()

# # Initialize LLaMA3 model
# llm = ChatGroq(model="gemma2-9b-it")


# # Define the graph state
# class State(TypedDict):
#     joke: str
#     topic: str
#     feedback: str


# # Function to generate a joke
# def llm_call_generator(state: State):
#     """LLM generates a joke"""
#     if state.get("feedback"):
#         msg = llm.invoke(
#             f"Write a joke about {state['topic']} but take into account the feedback: {state['feedback']}"
#         )
#     else:
#         msg = llm.invoke(f"Write a joke about {state['topic']}")
#     return {"joke": msg.content}


# # Build the workflow
# optimizer_builder = StateGraph(State)
# optimizer_builder.add_node("llm_call_generator", llm_call_generator)
# optimizer_builder.add_edge(START, "llm_call_generator")
# optimizer_builder.add_edge("llm_call_generator", END)
# optimizer_workflow = optimizer_builder.compile()

# # Streamlit UI
# st.title("AI Joke Generator 🤖😂")

# # Initialize session state variables
# if "topic" not in st.session_state:
#     st.session_state.topic = ""
# if "joke" not in st.session_state:
#     st.session_state.joke = ""
# if "feedback" not in st.session_state:
#     st.session_state.feedback = ""
# if "show_feedback_input" not in st.session_state:
#     st.session_state.show_feedback_input = False

# # User input for topic
# topic = st.text_input("Enter a topic for the joke:", st.session_state.topic)

# if st.button("Generate Joke"):
#     if topic:
#         state = optimizer_workflow.invoke({"topic": topic})
#         st.session_state.joke = state["joke"]
#         st.session_state.topic = topic
#         st.session_state.feedback = ""
#         st.session_state.show_feedback_input = False  # Reset feedback visibility
#         st.rerun()
#     else:
#         st.warning("Please enter a topic before generating a joke!")

# # Display the joke if available
# if st.session_state.joke:
#     st.subheader("Here's your joke:")
#     st.write(st.session_state.joke)

#     # Store radio selection in a local variable
#     user_review_status = st.radio(
#         "Enter review status (Accepted/Feedback):",
#         ["Accepted", "Feedback"],
#         index=None,
#         key="review_status",  # Use a different key name
#     )

#     # Handle user selection (without modifying `st.session_state` directly)
#     if user_review_status == "Accepted":
#         st.success("Glad you liked it! 🎉")
#         st.session_state.joke = ""
#         st.session_state.topic = ""
#         st.session_state.show_feedback_input = False  # Hide feedback input
#         st.rerun()

#     elif user_review_status == "Feedback":
#         if not st.session_state.show_feedback_input:
#             st.session_state.show_feedback_input = True
#             st.rerun()  # Force rerun to show feedback input

# if "jokes_history" not in st.session_state:
#     st.session_state.jokes_history = []  # Store all previous jokes

# if st.session_state.show_feedback_input:
#     feedback_text = st.text_input("What could be improved?", st.session_state.feedback)

#     if st.button("Submit Feedback"):
#         if feedback_text:
#             state = optimizer_workflow.invoke({"topic": feedback_text})
#             new_joke = state["joke"]
            
#             # Store only the first joke before updating
#             if "feedback_submitted" not in st.session_state:
#                 st.session_state.jokes_history.append(st.session_state.joke)

#             st.session_state.joke = new_joke  # Update to new joke
#             st.session_state.feedback = feedback_text
#             st.session_state.show_feedback_input = False  # Hide input
#             st.session_state.feedback_submitted = True  # Mark feedback as submitted
#             st.rerun()

# # ✅ Show the **original** joke before feedback
# if st.session_state.jokes_history:
#     st.subheader("Original Joke:")
#     st.write(st.session_state.jokes_history[0])  # Only show the first joke
#     st.write("---")

# # ✅ Show only the **latest joke after feedback**
# if st.session_state.joke:
#     st.subheader("Updated Joke:")
#     st.write(st.session_state.joke)


import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

# Load environment variables
load_dotenv()

# Initialize LLaMA3 model
llm = ChatGroq(model="gemma2-9b-it")

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
    st.session_state.show_feedback_input = False
if "updated_joke" not in st.session_state:
    st.session_state.updated_joke = ""  # Store feedback-based joke separately

# User input for topic
topic = st.text_input("Enter a topic for the joke:", st.session_state.topic)

if st.button("Generate Joke"):
    if topic:
        state = optimizer_workflow.invoke({"topic": topic})
        st.session_state.joke = state["joke"]  # Store only the first joke here
        st.session_state.topic = topic
        st.session_state.feedback = ""  # Reset feedback
        st.session_state.show_feedback_input = False  # Hide feedback input
        st.session_state.updated_joke = ""  # Clear updated joke
        st.rerun()
    else:
        st.warning("Please enter a topic before generating a joke!")

# ✅ Display only the original joke first
if st.session_state.joke:
    st.subheader("Here's your joke:")
    st.write(st.session_state.joke)

    # Radio button for review status
    user_review_status = st.radio(
        "Enter review status (Accepted/Feedback):",
        ["Accepted", "Feedback"],
        index=None,
        key="review_status"
    )

    # Handle user selection (only show feedback input if needed)
    if user_review_status == "Feedback":
        st.session_state.show_feedback_input = True
        st.rerun()

# ✅ Show feedback input only when "Feedback" is selected
if st.session_state.show_feedback_input:
    feedback_text = st.text_input("What could be improved?", st.session_state.feedback)

    if st.button("Submit Feedback"):
        if feedback_text:
            state = optimizer_workflow.invoke({"topic": st.session_state.topic, "feedback": feedback_text})
            st.session_state.updated_joke = state["joke"]  # Store feedback-based joke
            st.session_state.feedback = feedback_text  # Store feedback text
            st.session_state.show_feedback_input = False  # Hide input after submission
            st.rerun()
        else:
            st.warning("Please provide feedback before submitting!")

# ✅ Display updated joke separately, ONLY after feedback is submitted
if st.session_state.updated_joke:
    st.subheader("New Joke Based on Your Feedback:")
    st.write(st.session_state.updated_joke)
