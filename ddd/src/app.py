from langgraph.graph import StateGraph, START, END
from nodes import LifeCycleState
from nodes import get_user_requirements, create_user_stories

# Build workflow
optimizer_builder = StateGraph(LifeCycleState)

# Add nodes
optimizer_builder.add_node("get_user_requirements", get_user_requirements)
optimizer_builder.add_node("create_user_stories", create_user_stories)

# Add edges to connect nodes
optimizer_builder.add_edge(START, "get_user_requirements")
optimizer_builder.add_edge("get_user_requirements", "create_user_stories")
optimizer_builder.add_edge("create_user_stories", END)

# Compile
optimizer_workflow = optimizer_builder.compile()

# Save workflow
# optimizer_workflow.get_graph().draw_mermaid_png(output_file_path="software_life_cycle_workflow.png")

prompt = "I want to develop a user management system with two user types: Admin and User. Admins will have the ability to create, list, update, and delete users, while Users will only be able to retrieve their own details using their user ID."
state = optimizer_workflow.invoke({"prompt": prompt})
