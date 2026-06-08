import json
from pathlib import Path

PROFILE_FILE = Path("data/profiles.json")
SUMMARY_FILE = Path("data/summaries.json")


def load_json(path):
    if not path.exists():
        return {}

    with open(path, "r") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def get_profile(user_id):
    profiles = load_json(PROFILE_FILE)
    return profiles.get(user_id, {})


def save_profile(user_id, profile):
    profiles = load_json(PROFILE_FILE)
    profiles[user_id] = profile
    save_json(PROFILE_FILE, profiles)


def get_summary(session_id):
    summaries = load_json(SUMMARY_FILE)
    return summaries.get(session_id, "")


def save_summary(session_id, summary):
    summaries = load_json(SUMMARY_FILE)
    summaries[session_id] = summary
    save_json(SUMMARY_FILE, summaries)