import json
import re
import time
from infrastructure.bedrock_client import BedrockClient
from config.model_config import MODELS
from pathlib import Path

PROFILE_FILE = Path("data/profiles.json")
SUMMARY_FILE = Path("data/summaries.json")


def load_json(path):

    if not path.exists():
        return {}

    try:
        with open(path, "r") as f:
            return json.load(f)

    except Exception:
        return {}


def save_json(path, data):

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(path, "w") as f:
        json.dump(
            data,
            f,
            indent=4
        )


# ==================================================
# PROFILE MEMORY
# ==================================================

def get_profile(user_id):

    profiles = load_json(
        PROFILE_FILE
    )

    return profiles.get(
        user_id,
        {}
    )


def save_profile(
        user_id,
        profile
):

    profiles = load_json(
        PROFILE_FILE
    )

    profiles[user_id] = profile

    save_json(
        PROFILE_FILE,
        profiles
    )


def update_profile_from_message(
        user_id,
        message
):

    profile = get_profile(
        user_id
    )

    name_match = re.search(
        r"my name is (.+)",
        message.lower()
    )

    if name_match:

        profile["name"] = (
            name_match.group(1)
            .strip()
            .title()
        )

    save_profile(
        user_id,
        profile
    )


# ==================================================
# SUMMARY MEMORY
# ==================================================

def get_summaries(session_id):

    summaries = load_json(
        SUMMARY_FILE
    )

    return summaries.get(
        session_id,
        []
    )


def get_summary(session_id):

    summaries = get_summaries(
        session_id
    )

    if not summaries:
        return ""

    return "\n\n".join(
        [
            item["summary"]
            for item in summaries
        ]
    )


def save_summary(
        session_id,
        summary
):

    summaries = load_json(
        SUMMARY_FILE
    )

    if session_id not in summaries:
        summaries[session_id] = []

    summaries[session_id].append(
        {
            "timestamp": time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "summary": summary
        }
    )

    save_json(
        SUMMARY_FILE,
        summaries
    )
def generate_conversation_summary(messages):

    conversation_text = "\n".join(
        [
            f"{msg['role']}: {msg['content']}"
            for msg in messages
        ]
    )

    prompt = f"""
Summarize this conversation.

Focus on:

- Important user facts
- User preferences
- Important questions
- Important answers
- Things that may be useful later

Conversation:

{conversation_text}

Summary:
"""

    client = BedrockClient(
        MODELS.GENERAL
    )

    result = client.generate(
        prompt
    )

    return result["answer"]