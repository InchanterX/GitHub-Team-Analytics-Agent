from typing import Optional
from src.services.github_client.domain.protocols.github_repository import GitHubRepository
from src.services.github_client.models.commit import Commit


class AnalyticsService:
    def __init__(self, github_repo: GitHubRepository):
        self._github_repo = github_repo

    def analyze_commits(
        self,
        owner: str,
        repo: str,
        since: str,
        until: str
    ) -> dict:
        commits = self._github_repo.get_commits(owner, repo, since, until)

        return {
            "total": len(commits),
            "top_author": self._top_author(commits),
            "by_author": self._by_author(commits),
            "peak_day": self._peak_day(commits),
        }

    def _top_author(self, commits: list[Commit]) -> Optional[str]:
        author_commit_count = {}

        for commit in commits:
            author_commit_count[commit.author] = (
                author_commit_count.get(commit.author, 0) + 1
            )

        return (
            max(author_commit_count, key=author_commit_count.get)
            if author_commit_count
            else None
        )

    def _by_author(self, commits: list[Commit]) -> dict[str, int]:
        stats = {}

        for commit in commits:
            stats[commit.author] = stats.get(commit.author, 0) + 1

        return stats

    def _peak_day(self, commits: list[Commit]) -> Optional[str]:
        by_day = {}

        for commit in commits:
            day = commit.date[:10]
            by_day[day] = by_day.get(day, 0) + 1

        return max(by_day, key=by_day.get) if by_day else None

    def get_issue(self, owner: str, repo: str) -> list[dict]:
        return self._github_repo.get_issues(owner, repo)

    def summarize_commits(self, owner: str, repo: str, since: str, until: str) -> str:
        commits = self._github_repo.get_commits(owner, repo, since, until)

        if not commits:
            return "No commits found in the given period."

        summary = f"Total commits: {len(commits)}\n"
        summary += f"Top author: {self._top_author(commits)}\n"
        summary += f"Peak day: {self._peak_day(commits)}\n"

        return summary
