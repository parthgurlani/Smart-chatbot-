from typing import Type, Dict
from .base_agent import BaseAgent

class AgentRegistry:
    _agents: Dict[str, Type['BaseAgent']] = {}

    @classmethod
    def register(cls, domain: str):
        """Decorator to register an agent dynamically."""
        def wrapper(agent_class: Type['BaseAgent']):
            cls._agents[domain] = agent_class
            return agent_class
        return wrapper

    @classmethod
    def get_agent(cls, domain: str) -> Type['BaseAgent']:
        """Returns the specific agent, defaulting to general if not found."""
        return cls._agents.get(domain, cls._agents.get("general"))