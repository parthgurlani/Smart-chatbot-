import json
import re
from infrastructure.bedrock_client import BedrockClient
from config.model_config import MODELS


class RouterAgent:
    def __init__(self):
        self.client = BedrockClient(MODELS.ROUTER)

    def classify_intent(self, query: str) -> dict:
        prompt = f"""
        Analyze the query and classify it into exactly one of these domains:
        "medical", "coding", or "general".

        Determine if answering requires up-to-date,
        live web search (true/false).

        Respond ONLY with a raw JSON object.
        No markdown.

        Format:
        {{"domain":"string","needs_search":boolean}}

        Query: "{query}"
        """

        result = self.client.generate(prompt)

        # Extract actual text response
        response = result["answer"]

        try:
            clean_json = re.search(
                r'\{.*\}',
                response,
                re.DOTALL
            )

            if clean_json:
                return json.loads(clean_json.group())

            return json.loads(response)

        except Exception:
            print(
                f"Router Parse Error. "
                f"Fallback to general. Raw: {response}"
            )

            return {
                "domain": "general",
                "needs_search": False
            }