from src.services.github_client.domain.protocols.github_repository import GitHubRepository
from src.services.github_client.adapters.github.github_client import GitHubClient
from src.services.github_client.models.commit import Commit
from src.services.github_client.models.issue import Issue


class GitHubRepositoryImplementation(GitHubRepository):
    def __init__(self, client: GitHubClient):
        self._client = client

    def get_commits(self, owner: str, repo: str, since: str, until: str) -> list[Commit]:
        raw = self._client.get_commits(owner, repo, since, until)

        return [
            Commit(
                sha=commit['sha'],
                author=commit['author'],
                message=commit['message'],
                date=commit['date'],
                verified=commit.get('verified', False),
                files_changed=commit.get('files_changed', 0)
            ) for commit in raw
        ]

    def get_issues(self, owner: str, repo: str) -> list[Issue]:
        raw = self._client.get_issues(owner, repo)

        return [
            Issue(
                title=issue['title'],
                author=issue['author'],
                created_at=issue['created_at']
            ) for issue in raw
        ]
