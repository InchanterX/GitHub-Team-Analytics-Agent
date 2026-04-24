import json
from typing import Any
from loguru import logger


class Agent:
    def __init__(self, planner, executor, llm):
        self._planner = planner
        self._executor = executor
        self._llm = llm

    def run(self, query: str, params: dict[str, Any]) -> str:
        tools = self._planner.plan(query)
        logger.info(f"Planner selected tools: {tools}")

        data = self._executor.execute(tools, params)
        logger.info(
            f"Executor returned: {json.dumps(data, indent=2, default=str)}")

        formatted_data = json.dumps(
            data, indent=2, ensure_ascii=False, default=str)

        final_prompt = f"""You are a GitHub repository analyst. Analyze the provided data and answer the user's query.

User query: {query}

Repository data (REAL data, use it exactly as provided):
{formatted_data}

IMPORTANT INSTRUCTIONS:
- Use ONLY the data provided above, do NOT make up or guess any information
- If specific data is missing, say "not available" instead of making it up
- Reference exact numbers, dates, and names from the data
- Format dates exactly as they appear in the data
- Structure your response clearly

Provide analysis:"""

        logger.debug(f"Final prompt sent to LLM:\n{final_prompt}")

        response = self._llm.generate_response(final_prompt)
        return response
