import requests
from config.settings import BEDROCK_API_KEY, BEDROCK_BASE_URL


class BedrockClient:
    def __init__(self, model_name: str):
        self.model_name = model_name

    def generate(self, prompt: str):
        headers = {
            "Authorization": f"Bearer {BEDROCK_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
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

            # Uncomment for debugging if needed
            # print("\n===== BEDROCK RESPONSE =====")
            # print(data)
            # print("===========================\n")

            answer = data["choices"][0]["message"]["content"]

            usage = data.get("usage", {})

            # OpenAI-compatible format
            input_tokens = usage.get(
                "prompt_tokens",
                usage.get("input_tokens", 0)
            )

            output_tokens = usage.get(
                "completion_tokens",
                usage.get("output_tokens", 0)
            )

            total_tokens = usage.get(
                "total_tokens",
                input_tokens + output_tokens
            )

            return {
                "success": True,
                "answer": answer,
                "model": self.model_name,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens,
                "raw_response": data
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "answer": "System Error: Request timed out.",
                "model": self.model_name,
                "input_tokens": 0,
                "output_tokens": 0,
                "total_tokens": 0
            }

        except requests.exceptions.HTTPError as e:
            return {
                "success": False,
                "answer": f"HTTP Error: {str(e)}",
                "model": self.model_name,
                "input_tokens": 0,
                "output_tokens": 0,
                "total_tokens": 0
            }

        except Exception as e:
            return {
                "success": False,
                "answer": f"System Error: Bedrock API unavailable ({str(e)})",
                "model": self.model_name,
                "input_tokens": 0,
                "output_tokens": 0,
                "total_tokens": 0
            }