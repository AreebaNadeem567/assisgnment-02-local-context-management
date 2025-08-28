import os
from dotenv import load_dotenv
from agents import OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig

# Load environment variables
load_dotenv()

# Get Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Check API key
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set.")

# Initialize async client
client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Configure the model
config = RunConfig(
    model=OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=client
    ),
    model_provider=client,
    tracing_disabled=True
)