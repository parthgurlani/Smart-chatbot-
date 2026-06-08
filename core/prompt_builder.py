from core.memory_manager import (
    get_profile,
    get_summary
)

from core.session_manager import (
    get_recent_messages
)


def build_prompt(
        user_id,
        session_id,
        current_message
):

    profile = get_profile(user_id)

    summary = get_summary(
        session_id
    )

    recent = get_recent_messages(
        session_id
    )

    return f"""
You are a helpful AI assistant.

User Profile:
{profile}

Conversation Summary:
{summary}

Recent Messages:
{recent}

Current User Message:
{current_message}
"""