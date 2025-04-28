from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

# Load env vars
load_dotenv()


class LLM:
    def __init__(self):
        pass

    def initialize_llm(self, name):
        """Initializes and returns an LLM model based on the given name."""
        if name == "openai":
            return ChatOpenAI(model="gpt-4o", temperature=0)
        elif name == "llama":
            return ChatGroq(model="llama3-70b-8192", temperature=0)
        else:
            raise ValueError(f"Unsupported LLM name: {name}")
