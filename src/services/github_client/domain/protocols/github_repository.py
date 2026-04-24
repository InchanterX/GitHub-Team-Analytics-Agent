from typing import Protocol
from src.services.github_client.models.commit import Commit
from src.services.github_client.models.issue import Issue


class GitHubRepository(Protocol):
    def get_commits(self, owner: str, repo: str, since: str, until: str) -> list[Commit]:
        ...

    def get_issues(self, owner: str, repo: str) -> list[Issue]:
        ...
