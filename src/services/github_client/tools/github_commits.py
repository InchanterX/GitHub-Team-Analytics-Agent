from src.services.github_client.domain.analytics_service import AnalyticsService


class CommitTool:
    def __init__(self, analytics: AnalyticsService):
        self._analytics = analytics

    def run(self, params: dict) -> dict:
        return self._analytics.analyze_commits(**params)
