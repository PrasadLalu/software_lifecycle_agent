from dotenv import load_dotenv
from langchain_groq import ChatGroq
from src.state.user_stories import UserStories

load_dotenv()


model = ChatGroq(model="llama3-70b-8192", temperature=0)
user_story_evaluator = model.with_structured_output(UserStories)

def evaluate_user_stories(query: str) -> UserStories:
    """Generate user stories from a query using the evaluator."""
    return user_story_evaluator(query)