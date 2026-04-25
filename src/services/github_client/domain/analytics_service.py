from typing import Optional
from src.services.github_client.domain.protocols.github_repository import GitHubRepository
from src.services.github_client.models.commit import Commit


class AnalyticsService:
    def __init__(self, github_repo: GitHubRepository):
        self._github_repo = github_repo

    def analyze_commits(self, owner: str, repo: str, since: str, until: str) -> dict:
        commits = self._github_repo.get_commits(owner, repo, since, until)

        if not commits:
            return {"total": 0, "message": "No commits found"}

        verified_count = sum(1 for c in commits if c.verified)
        total_files_changed = sum(c.files_changed for c in commits)

        return {
            "total": len(commits),
            "top_author": self._top_author(commits),
            "by_author": self._by_author(commits),
            "peak_day": self._peak_day(commits),
            "verified_commits": f"{verified_count}/{len(commits)}",
            "total_files_changed": total_files_changed,
            "recent_commits": [
                {
                    "date": commit.date[:10],
                    "author": commit.author,
                    "message": commit.message[:100],
                    "verified": commit.verified,
                    "files_changed": commit.files_changed
                }
                for commit in commits[:50]
            ],
            "date_range": f"{commits[-1].date[:10]} to {commits[0].date[:10]}" if commits else "unknown"
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

    def analyze_issues(self, owner: str, repo: str) -> dict:
        issues = self._github_repo.get_issues(owner, repo)

        return {
            "total": len(issues),
            "by_author": self._count_by_author(issues),
            "open_issues": len([i for i in issues if hasattr(i, 'state') and i.state == 'open'])
        }

    def _count_by_author(self, items: list) -> dict[str, int]:
        stats = {}
        for item in items:
            stats[item.author] = stats.get(item.author, 0) + 1
        return stats
