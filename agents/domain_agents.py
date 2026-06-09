from agents.registry import AgentRegistry
from agents.base_agent import BaseAgent
from config.model_config import MODELS

@AgentRegistry.register("medical")
class MedicalAgent(BaseAgent):
    def __init__(self):
        super().__init__(MODELS.MEDICAL, "medical")

@AgentRegistry.register("coding")
class CodingAgent(BaseAgent):
    def __init__(self):
        super().__init__(MODELS.CODING, "coding")

@AgentRegistry.register("general")
class GeneralAgent(BaseAgent):
    def __init__(self):
        super().__init__(MODELS.GENERAL, "general")