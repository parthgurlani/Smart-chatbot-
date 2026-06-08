import json
from pathlib import Path

SESSION_FILE = Path("data/sessions.json")

MAX_RECENT_MESSAGES = 10

def load_sessions():
    if not SESSION_FILE.exists():
        return {}

    with open(SESSION_FILE, "r") as f:
        return json.load(f)


def save_sessions(data):
    with open(SESSION_FILE, "w") as f:
        json.dump(data, f, indent=4)


def add_message(session_id, role, content):
    sessions = load_sessions()

    sessions.setdefault(session_id, [])

    sessions[session_id].append({
        "role": role,
        "content": content
    })

    save_sessions(sessions)


def get_recent_messages(session_id):
    sessions = load_sessions()

    messages = sessions.get(session_id, [])

    return messages[-MAX_RECENT_MESSAGES:]