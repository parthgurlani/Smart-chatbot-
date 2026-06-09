import os
from dotenv import load_dotenv

load_dotenv()

BEDROCK_API_KEY = os.getenv(
    "BEDROCK_API_KEY"
)

BEDROCK_BASE_URL = os.getenv(
    "BEDROCK_BASE_URL"
)

DEFAULT_MODEL = os.getenv(
    "DEFAULT_MODEL",
    "claude-sonnet"
)
