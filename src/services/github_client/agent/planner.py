import json
from src.services.github_client.domain.protocols.llm_provider import LLMProvider


class Planner:
    def __init__(self, llm: LLMProvider):
        self._llm = llm

    def plan(self, query: str) -> list[str]:
        prompt = f"""
        You are a planner. Decide which tools to use for the query.
        Return ONLY a JSON array of tool names, no explanation.
        Available tools: commits, issues, summary.
        Query: {query}
        """
        response = self._llm.generate_response(prompt)
        try:
            return json.loads(response)
        except Exception:
            return []
