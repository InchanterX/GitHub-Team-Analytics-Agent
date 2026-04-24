from openai import OpenAI
from loguru import logger


class OpenAIClient:
    def __init__(self, api_key: str, base_url: str = None, model: str = "gpt-4"):
        if not api_key:
            api_key = "not-needed"

        logger.debug(
            f"Initializing OpenAI client with base_url={base_url}, model={model}")

        self._client = OpenAI(api_key=api_key, base_url=base_url)
        self._model = model

    def create_chat_completion(self, prompt: str):
        logger.debug(f"Creating chat completion with model={self._model}")
        return self._client.chat.completions.create(
            model=self._model,
            messages=[{"role": "user", "content": prompt}]
        )
