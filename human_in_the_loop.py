import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import tools_condition, ToolNode

# Load environment variables
load_dotenv()

# Initialize AI Model
llm = ChatGroq(model="gemma2-9b-it")

# Define arithmetic operations
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b

def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b

def divide(a: int, b: int) -> float:
    """Divide two integers, returning a float."""
    return a / b

# Bind tools to the model
tools = [add, multiply, divide]
llm_with_tools = llm.bind_tools(tools)

# Define assistant logic
sys_msg = SystemMessage(content="You are a helpful assistant tasked with performing arithmetic.")

def assistant(state: MessagesState):
    """Processes user input and returns an AI-generated response."""
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

# Build execution graph
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

# builder.add_edge(START, "assistant")
# builder.add_conditional_edges("assistant", tools_condition)
# builder.add_edge("tools", "assistant")
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", "assistant")


memory = MemorySaver()
graph = builder.compile(interrupt_before=["tools"], checkpointer=memory)

# Streamlit UI
st.title("Arithmetic Assistant with Human Feedback")
user_input = st.text_input("Enter an arithmetic expression:", value="Multiply 2 and 3")

if 'response' not in st.session_state:
    st.session_state.response = ""
if 'feedback_response' not in st.session_state:
    st.session_state.feedback_response = ""
if 'thread' not in st.session_state:
    st.session_state.thread = None

if st.button("Submit"):
    if user_input:
        st.session_state.thread = {"configurable": {"thread_id": "1"}}
        initial_input = {"messages": HumanMessage(content=user_input)}
        
        debug_log = ""
        for event in graph.stream(initial_input, st.session_state.thread, stream_mode="values"):
            debug_log += f"Event received: {event}\n"
            if 'messages' in event and event['messages']:
                st.session_state.response = event['messages'][-1].content
            else:
                st.session_state.response = "Error: No response received."
        
        st.text(debug_log)  # Print debug info

st.write("### AI Response:")
if st.session_state.response.strip():
    st.success(st.session_state.response)
else:
    st.error("No response received. Please try again.")

# Collect feedback
feedback = st.radio("Was this answer helpful?", ("👍 Yes", "👎 No"), index=None)
if feedback and st.session_state.thread:
    st.write("Thank you for your feedback!")
    feedback_input = {"messages": HumanMessage(content=f"User feedback: {feedback}")}
    debug_feedback_log = ""
    for event in graph.stream(feedback_input, st.session_state.thread, stream_mode="values"):
        debug_feedback_log += f"Feedback Event: {event}\n"
        if 'messages' in event and event['messages']:
            st.session_state.feedback_response = event['messages'][-1].content
        else:
            st.session_state.feedback_response = "No response received."
    
    st.write("### AI Response to Feedback:")
    st.success(st.session_state.feedback_response)
    st.text(debug_feedback_log)  # Print debug info

