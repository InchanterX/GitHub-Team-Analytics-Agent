from openai import OpenAI


class OpenAIClient:
    def __init__(self, api_key: str, base_url: str = None, model: str = "gpt-4"):
        self._client = OpenAI(api_key=api_key, base_url=base_url)
        self._model = model

    def create_chat_completion(self, prompt: str):
        return self._client.chat.completions.create(
            model=self._model,
            messages=[{"role": "user", "content": prompt}]
        )
