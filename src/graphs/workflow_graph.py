from langgraph.graph import StateGraph, START, END
from src.state.agent_state import LifeCycleState
from src.nodes.user_requirement import get_user_requirement
from src.nodes.user_story import create_user_stories


def build_workflow():
    """Build the workflow graph."""

    # Build workflow
    workflow_builder = StateGraph(LifeCycleState)

    # Add nodes
    workflow_builder.add_node("user_requirement", get_user_requirement)
    workflow_builder.add_node('create_user_stories', create_user_stories)

    # Add edges to connect nodes
    workflow_builder.add_edge(START, "user_requirement")
    workflow_builder.add_edge("user_requirement", "create_user_stories")
    workflow_builder.add_edge("create_user_stories", END)

    return workflow_builder.compile()
