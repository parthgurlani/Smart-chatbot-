from models.bedrock_client import (
    BedrockClient
)

client = BedrockClient()

response = client.generate(
    "What is 2 + 2?"
)

print(response)