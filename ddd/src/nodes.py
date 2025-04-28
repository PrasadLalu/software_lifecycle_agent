from typing import List
from typing_extensions import TypedDict
from pydantic import BaseModel, Field

from tools import Tool
from llms import LLM

# Jira Tool
tool = Tool()
jira = tool.get_jira_tool()

# Initialize Llama model
llm = LLM()
model = llm.initialize_llm("llama")

class UserStory(BaseModel):
    title: str = Field(
        description="Title of the user story summarizing the functionality."
    )
    description: str = Field(
        description="Detailed user story following the format: 'As a [user], I want to [action] so that [benefit]'."
    )
    acceptance_criteria: List[str] = Field(
        description="List of acceptance criteria that define when this story is complete."
    )


class UserStories(BaseModel):
    stories: List[UserStory] = Field(
        default_factory=list, description="List of generated user stories."
    )
    
# UserStory schema for structured output
user_story_evaluator = model.with_structured_output(UserStories)

class LifeCycleState(TypedDict):
    prompt: str
    content: str
    user_stories: UserStories


def get_user_requirements(state: LifeCycleState):
    """Generates structured user stories from user requirements using the `UserStories` schema."""
    result = user_story_evaluator.invoke(
        f"Split the following requirements into distinct user stories. "
        f"Each user story should include a title, description, and acceptance criteria: {state['prompt']}"
    )
    return {"user_stories": result}


def create_user_stories(state: LifeCycleState):
    if not state["user_stories"].stories:
        print("No user stories found.")
        return

    for story in state["user_stories"].stories:
        jira.create_user_story(
            title=story.title,
            description=story.description,
            acceptance_criteria=story.acceptance_criteria,
        )
        
    return state