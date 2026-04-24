from openai import OpenAI


class OpenAIClient:
    def __init__(self, api_key: str):
        self._client = OpenAI(api_key=api_key)

    def create_chat_completion(self, prompt: str):
        return self._client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
