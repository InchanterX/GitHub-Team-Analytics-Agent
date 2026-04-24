import json
from src.services.github_client.domain.protocols.llm_provider import LLMProvider


class Planner:
    def __init__(self, llm: LLMProvider):
        self._llm = llm

    def plan(self, query: str) -> list[str]:
        prompt = f"""
        Decide which tools to use.

        Query: {query}

        Tools:
        - commits
        - issues
        - summary

        Return JSON list.
        """
        response = self._llm.generate_response(prompt)
        try:
            return json.loads(response)
        except Exception:
            return []
