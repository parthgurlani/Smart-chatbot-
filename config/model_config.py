from dataclasses import dataclass

@dataclass(frozen=True)
class ModelAssignments:
    MEDICAL: str = "us.anthropic.claude-sonnet-4-6"
    CODING: str = "qwen.qwen3-coder-next"
    GENERAL: str = "us.amazon.nova-lite-v1:0"
    ROUTER: str = "us.amazon.nova-micro-v1:0"
    

MODELS = ModelAssignments()