import json
from loguru import logger
from src.services.github_client.domain.protocols.llm_provider import LLMProvider


class Planner:
    def __init__(self, llm: LLMProvider):
        self._llm = llm

    def plan(self, query: str) -> list[str]:
        prompt = f"""You are a task planner. Select ONLY tools directly relevant to the query.

    Available tools:
    - "commits": commit history, authors, code changes, development activity
    - "issues": open issues, bug reports, feature requests
    - "summary": comprehensive overview, general project analysis, "tell me about the project"

    CRITICAL RULES:
    - Select ONLY what the user explicitly asks for
    - "Analyze commit activity" → ONLY ["commits"]
    - "Show issues" → ONLY ["issues"]
    - "Repository overview" or "general analysis" → ["commits", "issues"]
    - If the query mentions ONLY commits → do NOT include "issues"
    - If the query mentions ONLY issues → do NOT include "commits"
    - Return ONLY a JSON array: ["commits"] or ["issues"] or ["commits", "issues"]

    User query: {query}

    Tools to use (JSON array):"""

        try:
            response = self._llm.generate_response(prompt)
            logger.debug(f"Planner raw response: {response}")

            response = response.strip()
            if response.startswith("```"):
                response = response.split('\n')[1:]
                response = '\n'.join(response[:-1])

            tools = json.loads(response)
            logger.info(f"Planner selected tools: {tools}")

            if not tools:
                logger.warning("Planner returned empty list, using defaults")
                return ["commits", "issues"]

            return tools

        except Exception as e:
            logger.error(f"Planner failed: {e}, using defaults")
            return ["commits", "issues"]  # fallback
