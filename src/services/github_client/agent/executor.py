from typing import Any


class Executor:
    def __init__(self, tools: dict):
        self._tools = tools

    def execute(self, tools_names: list[str], params: dict[str, Any]) -> str:
        result = {}

        for tool in tools_names:
            if tool in self._tools:
                result[tool] = self._tools[tool].run(params)

        return result
