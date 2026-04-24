# planner.py
import json
from loguru import logger
from src.services.github_client.domain.protocols.llm_provider import LLMProvider


class Planner:
    def __init__(self, llm: LLMProvider):
        self._llm = llm

    def plan(self, query: str) -> list[str]:
        prompt = f"""You are a task planner for a GitHub analytics agent.

Available tools and when to use them:
- "commits" - Use for ANY query about commits, development activity, contributions, code changes, authors, or repository history
- "issues" - Use for ANY query about issues, bugs, problems, feature requests, or open tasks
- "summary" - Use when the user wants a comprehensive overview or summary combining multiple aspects

Rules:
- ALWAYS return at least one tool, never an empty list
- If the query mentions commits, activity, changes, or development → include "commits"
- If the query mentions issues, bugs, or problems → include "issues"
- If the query is vague or asks for general analysis → use ["commits", "issues"]
- Return ONLY a JSON array, no explanation

User query: {query}

Return JSON array of tools:"""

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
