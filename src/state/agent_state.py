from typing_extensions import TypedDict
from src.state.user_stories import UserStories


class LifeCycleState(TypedDict):
    prompt: str
    user_stories: UserStories
