from src.services.github_client.domain.analytics_service import AnalyticsService
from src.services.github_client.domain.protocols.llm_provider import LLMProvider
from loguru import logger


class DiffSummaryTool:
    def __init__(self, analytics: AnalyticsService, llm: LLMProvider):
        self._analytics = analytics
        self._llm = llm

    def run(self, params: dict) -> str:
        commits_data = self._analytics.analyze_commits(
            owner=params["owner"],
            repo=params["repo"],
            since=params["since"],
            until=params["until"]
        )

        issues_data = self._analytics.analyze_issues(
            owner=params["owner"],
            repo=params["repo"]
        )

        commit_messages = [
            c.get("message", "")
            for c in commits_data.get("recent_commits", [])
        ]

        prompt = f"""
        Summarize the repository activity:

        Total commits: {commits_data.get('total', 0)}
        Top author: {commits_data.get('top_author', 'N/A')}
        Peak day: {commits_data.get('peak_day', 'N/A')}
        Total open issues: {issues_data.get('total', 0)}

        Recent commit messages:
        {chr(10).join(commit_messages[:10])}

        Provide a concise summary of the development activity.
        """

        return self._llm.generate_response(prompt)
