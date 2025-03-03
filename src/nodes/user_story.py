from src.state.agent_state import LifeCycleState
from src.tools.create_user_story import create_user_story

def create_user_stories(state: LifeCycleState):
    if not state["user_stories"].stories:
        print("No user stories found.")
        return

    for story in state["user_stories"].stories:
        print(f"Title: {story.title}")
        create_user_story(
            title=story.title,
            description=story.description,
            acceptance_criteria=story.acceptance_criteria,
        )
        
    return state