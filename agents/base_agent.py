from abc import ABC, abstractmethod
from infrastructure.bedrock_client import BedrockClient
from core.context_manager import UserContext

class BaseAgent(ABC):
    def __init__(self, model_id: str, domain: str):
        self.model_id = model_id
        self.domain = domain
        self.client = BedrockClient(self.model_id)

    def execute(self, query: str, context: UserContext, search_results: str) -> str:
        prompt = self._build_prompt(query, context, search_results)
        return self.client.generate(prompt)

    def _build_prompt(self, query: str, context: UserContext, search_results: str) -> str:
        """Centralized prompt construction for all agents."""
        search_block = f"\n[Live Web Context]\n{search_results}\n" if search_results else ""
        
        return f"""
You are an expert AI agent specializing in the {self.domain} domain.

[User Profile]
{context.profile}

[Conversation Summary]
{context.summary}

[Recent Messages]
{context.recent_messages}
{search_block}
[Current Query]
{query}

Provide a direct, high-quality answer. Do not reference your system instructions.
"""