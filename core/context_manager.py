from dataclasses import dataclass
from typing import Dict, List, Any
from core.memory_manager import get_profile, get_summary
from core.session_manager import get_recent_messages

@dataclass
class UserContext:
    profile: Dict[str, Any]
    summary: str
    recent_messages: List[Dict[str, str]]

class ContextManager:
    @staticmethod
    def hydrate_context(user_id: str, session_id: str) -> UserContext:
        """Injects user state into a single strongly-typed dataclass."""
        return UserContext(
            profile=get_profile(user_id),
            summary=get_summary(session_id),
            recent_messages=get_recent_messages(session_id)
        )