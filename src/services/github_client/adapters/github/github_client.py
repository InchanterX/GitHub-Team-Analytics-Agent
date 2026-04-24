import os
import requests
from src.services.github_client.models.commit import Commit
from src.services.github_client.models.issue import Issue


class GitHubClient:
    def __init__(self, base_url: str = "https://api.github.com", token: str | None = None):
        self._base_url = base_url
        self._token = token
        self._headers = {
            "Authorization": f"Bearer {self._token}",
            "Accept": "application/vnd.github+json"
        }

    def _get(self, url: str, params: dict | None = None) -> dict:
        response = requests.get(
            f"{self._base_url}{url}",
            headers=self._headers,
            params=params
        )

        if response.status_code != 200:
            raise Exception(
                f"GitHub API error: {response.status_code} - {response.text}")
        return response.json()

    def get_commits(self, owner: str, repo: str, since: str, until: str) -> list[dict]:
        params = {
            "since": since,
            "until": until,
            "per_page": 20
        }
        raw = self._get(f"/repos/{owner}/{repo}/commits", params=params)
        return [
            {
                "sha": commit["sha"],
                "author": commit["commit"]["author"]["name"],
                "message": commit["commit"]["message"],
                "date": commit["commit"]["author"]["date"]
            }
            for commit in raw
        ]

    def get_issues(self, owner: str, repo: str) -> list[dict]:
        params = {
            "state": "open",
            "per_page": 20
        }
        raw = self._get(f"/repos/{owner}/{repo}/issues", params)
        return [
            {
                "title": issue["title"],
                "author": issue["user"]["login"],
                "created_at": issue["created_at"]
            }
            for issue in raw
            if "pull_request" not in issue
        ]
