import json
from pathlib import Path

SESSION_FILE = Path("data/sessions.json")

MAX_RECENT_MESSAGES = 4
SUMMARY_TRIGGER = 4
KEEP_AFTER_SUMMARY = 2


def load_sessions():

    if not SESSION_FILE.exists():
        return {}

    try:
        with open(SESSION_FILE, "r") as f:
            return json.load(f)

    except Exception:
        return {}


def save_sessions(data):

    SESSION_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(SESSION_FILE, "w") as f:
        json.dump(
            data,
            f,
            indent=4
        )


def add_message(
        session_id,
        role,
        content
):

    sessions = load_sessions()

    sessions.setdefault(
        session_id,
        []
    )

    sessions[session_id].append(
        {
            "role": role,
            "content": content
        }
    )

    save_sessions(
        sessions
    )


def get_messages(
        session_id
):

    sessions = load_sessions()

    return sessions.get(
        session_id,
        []
    )


def get_recent_messages(
        session_id
):

    messages = get_messages(
        session_id
    )

    return messages[
        -MAX_RECENT_MESSAGES:
    ]


def trim_session(
        session_id,
        keep_last=KEEP_AFTER_SUMMARY
):

    print(f"\n=== TRIM SESSION ===")
    print(f"Session ID: {session_id}")
    print(f"Keep Last: {keep_last}")

    sessions = load_sessions()

    if session_id not in sessions:
        print("Session not found!")
        return

    print(f"Before Trim: {len(sessions[session_id])} messages")

    sessions[session_id] = (
        sessions[session_id][-keep_last:]
    )

    print(f"After Trim: {len(sessions[session_id])} messages")

    save_sessions(sessions)

    print("Session saved successfully")
    print("====================\n")


def should_summarize(
        session_id
):

    messages = get_messages(
        session_id
    )

    return (
        len(messages)
        >= SUMMARY_TRIGGER
    )