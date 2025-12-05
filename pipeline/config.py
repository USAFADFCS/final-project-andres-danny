import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY not found! Please create a .env file with your API key:\n"
        "OPENAI_API_KEY=sk-your-key-here"
    )

# Path resolver for project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def project_path(relative: str) -> str:
    """
    Resolves any relative path to its absolute path within the project.
    
    Example:
        project_path("cs110_docs") -> /full/path/to/project/cs110_docs
    """
    return os.path.join(PROJECT_ROOT, relative)


# Model configuration
MODEL_NAME = "gpt-4o-mini"  # Use mini for cost savings