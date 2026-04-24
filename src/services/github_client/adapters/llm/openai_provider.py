from src.services.github_client.domain.protocols.llm_provider import LLMProvider
from src.services.github_client.adapters.openai.openai_client import OpenAIClient


class OpenAIProvider(LLMProvider):
    def __init__(self, client: OpenAIClient):
        self._client = client

    def generate_response(self, prompt: str) -> str:
        response = self._client.create_chat_completion(prompt)
        return response.choices[0].message.content
