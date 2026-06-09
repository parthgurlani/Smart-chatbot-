import requests
from config.settings import BEDROCK_API_KEY, BEDROCK_BASE_URL

class BedrockClient:
    def __init__(self, model_name: str):
        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {BEDROCK_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}]
        }
        try:
            response = requests.post(
                BEDROCK_BASE_URL,
                json=payload,
                headers=headers,
                timeout=60
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"System Error: Bedrock API unavailable ({str(e)})"