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

        final_prompt = f"""You are a GitHub repository analyst. Answer using ONLY the provided data.

User query: {query}

Repository data:
{formatted_data}

CRITICAL FORMATTING RULES:
- NO markdown tables, no |---|---|
- NO markdown formatting (no **bold**, no ### headers, no --- lines)
- NO bullet points with dashes or numbers
- Use plain text with simple line breaks between sections

LENGTH: Aim for 20-25 lines total.

STRUCTURE:
Start with key metrics (2-3 lines):
- Total commits, time period, top contributor, open issues
- Brief context about the project scale

Then activity analysis (5-7 lines):
- How commits are distributed over time
- What the peak day reveals
- Types of commits and what they indicate about development focus
- Any patterns worth noting

Contributor insights (3-4 lines):
- Who contributed and their share
- What this suggests about the team

Issues status (2-3 lines):
- Open issues count and what it means
- If zero, simply note it and move on

Overall assessment (3-4 lines):
- What phase the project appears to be in
- Key strengths or concerns visible in the data
- Brief summary statement

Be specific with numbers but add brief interpretation. If data is missing, say so clearly but don't over-explain.

ANALYZE THE DATA NOW:"""

        logger.debug(f"Final prompt sent to LLM:\n{final_prompt}")

        response = self._llm.generate_response(final_prompt)
        return response
