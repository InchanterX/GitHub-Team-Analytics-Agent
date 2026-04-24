from typing import Any


class Agent:
    def __init__(self, planner, executor, llm):
        self._planner = planner
        self._executor = executor
        self._llm = llm

    def run(self, query: str, params: dict[str, Any]) -> str:
        tools = self._planner.plan(query)
        data = self._executor.execute(tools, params)

        final_prompt = f"""
        User query: {query}

        Data:
        {data}

        Provide insights.
        """

        return self._llm.generate_response(final_prompt)
