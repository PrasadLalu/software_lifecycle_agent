import streamlit as st
from typing import List, TypedDict
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

# Initialize the LLM
llm = ChatGroq(model="llama3-70b-8192")


class UserStory(BaseModel):
    """Represents a single user story, a key element in Agile software development methodologies like Jira."""
    title: str = Field(description="Title of the user story summarizing the functionality.")
    description: str = Field(description="Detailed explanation of the user story, providing context and elaborating on the desired outcome.")
    acceptance_criteria: List[str] = Field(description="List of acceptance criteria that define when this story is complete.")


class UserStories(BaseModel):
    stories: List[UserStory] = Field(default_factory=list, description="List of generated user stories.")


# Properly initialize session state variables
if "stories" not in st.session_state:
    st.session_state.stories = []  

if "state" not in st.session_state:
    st.session_state.state = {}

if "user_stories_review_status" not in st.session_state:
    st.session_state.user_stories_review_status = "Pending"

if "user_stories_feedback" not in st.session_state:
    st.session_state.user_stories_feedback = ""

# UserStory schema for structured output
user_story_evaluator = llm.with_structured_output(UserStories)


# Graph state
class State(TypedDict):
    requirement: str
    user_stories: UserStories
    user_stories_review_status: str


def create_user_stories(state: State):
    """Generates structured user stories from user requirement using the `UserStories` schema."""
    result = user_story_evaluator.invoke(
        f"Split the following requirement into distinct user stories. "
        f"Each user story should include a title, description, and acceptance criteria: {state['requirement']}"
    )
    return {"user_stories": result, "user_stories_review_status": "Pending Review"}


def review_user_stories(state: State):
    """Reviews the generated user stories based on the requirement and feedback."""
    if st.session_state.user_stories_feedback:
        return {"user_stories_review_status": "Feedback"}
    return {"user_stories_review_status": "Approved"}


def revise_user_stories(state: State):
    """Revises user stories based on feedback."""
    feedback = st.session_state.user_stories_feedback
    revised_result = llm.invoke(
        f"Revise the following user stories based on the given feedback:\n\nRequirement:\n{state['requirement']}\n\n"
        f"Feedback:\n{feedback}\n\nUser Stories:\n{state['user_stories']}"
    )
    return {"user_stories": revised_result, "user_stories_review_status": "Revised"}


def generate_code(state: State):
    """Placeholder function to generate code based on revised user stories."""
    pass


def route_review_user_stories(state: State):
    """Routes to the next step based on review status."""
    if state["user_stories_review_status"] == "Approved":
        return "Approved"
    elif state["user_stories_review_status"] == "Feedback":
        return "Feedback"


workflow_builder = StateGraph(State)

workflow_builder.add_node("create_user_stories", create_user_stories)
workflow_builder.add_node("review_user_stories", review_user_stories)
workflow_builder.add_node("revise_user_stories", revise_user_stories)
workflow_builder.add_node("generate_code", generate_code)

workflow_builder.add_edge(START, "create_user_stories")
workflow_builder.add_edge("create_user_stories", "review_user_stories")

workflow_builder.add_conditional_edges(
    "review_user_stories",
    route_review_user_stories,
    {
        "Approved": "generate_code",
        "Feedback": "revise_user_stories"
    }
)

workflow_builder.add_edge("revise_user_stories", "review_user_stories")
workflow_builder.add_edge("generate_code", END)

# Compile workflow builder
graph = workflow_builder.compile()

try:
    graph.get_graph().draw_mermaid_png(output_file_path="workflow.png")
except Exception:
    pass

default = """I want to develop a user management system with two user types: Admin and User.
Admins will have the ability to create, list, update, and delete users,
while Users will only be able to retrieve their own details using their user ID."""
requirement = st.text_area("Enter your requirement: ", value=default)


if st.button("Generate"):
    if requirement:
        st.session_state.state = graph.invoke({"requirement": requirement})
        
        if "user_stories" in st.session_state.state:
            st.session_state.stories = st.session_state.state["user_stories"].stories
        
        st.session_state.user_stories_review_status = "Pending Review"
    else:
        st.warning("Please enter your requirement...")


if st.session_state.stories:
    st.write("## Current User Stories:")
    for i, story in enumerate(st.session_state.stories):
        st.write(f"**{i+1}. {story.title}**")
        st.write(story.description)
        st.write("**Acceptance Criteria:**")
        for ac in story.acceptance_criteria:
            st.write(f"- {ac}")

    # User feedback section
    st.write("### Review User Stories")
    rating_options = ["Approved", "Feedback"]

    # Use a key to force re-rendering of the radio button
    radio_key = f"user_story_review_{len(st.session_state.stories)}"

    # Set default value for radio button
    default_index = rating_options.index(st.session_state.user_stories_review_status) if st.session_state.user_stories_review_status in rating_options else 0

    st.session_state.user_stories_review_status = st.radio(
        "Select rating:",
        rating_options,
        key=radio_key,
        index=default_index,
    )

    if st.session_state.user_stories_review_status == "Approved":
        st.success("User stories approved. Proceeding to code generation.")
    elif st.session_state.user_stories_review_status == "Feedback":
        user_stories_feedback = st.text_area("Your feedback:", key="user_stories_feedback")

        if st.button("Submit Feedback"):
            if user_stories_feedback:
                st.write(user_stories_feedback)
