from src.services.github_client.domain.analytics_service import AnalyticsService


class IssueTool:
    def __init__(self, analytics: AnalyticsService):
        self._analytics = analytics

    def run(self, params: dict) -> dict:
        return self._analytics.analyze_issues(
            owner=params["owner"],
            repo=params["repo"]
        )
