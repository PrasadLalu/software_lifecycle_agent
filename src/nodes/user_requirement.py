from dotenv import load_dotenv
from langchain_groq import ChatGroq
from src.state.user_stories import UserStories
from src.state.agent_state import LifeCycleState

load_dotenv()

model = ChatGroq(model="llama3-70b-8192", temperature=0)

# UserStory schema for structured output
user_story_evaluator = model.with_structured_output(UserStories)

def get_user_requirement(state: LifeCycleState):
    """Generates structured user stories from user requirements using the `UserStories` schema."""
    result = user_story_evaluator.invoke(
        f"Split the following requirements into distinct user stories. "
        f"Each user story should include a title, description, and acceptance criteria: {state['prompt']}"
    )
    return {"user_stories": result}
