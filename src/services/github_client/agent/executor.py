from typing import Any
from unittest import result
from src.services.github_client.domain.analytics_service import AnalyticsProvider


class Executor:
    def __init__(self, analytics: AnalyticsProvider):
        self._analytics = analytics

    def execute(self, tools: list[str], params: dict[str, Any]) -> str:
        result = {}

        if "commits" in tools:
            result["commits"] = self._analytics.analyze_commits(**params)

        if "issues" in tools:
            result["issues"] = self._analytics.get_issue(
                params["owner"],
                params["repo"]
            )

        if "summary" in tools:
            result["summary"] = self._analytics.summarize_commits(**params)

        return result
