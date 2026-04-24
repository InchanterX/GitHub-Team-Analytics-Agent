import os
import requests
from loguru import logger


class GitHubClient:
    def __init__(self, base_url: str, token: str):
        self._base_url = base_url
        self._token = token

        if not self._token:
            logger.error("GITHUB_TOKEN is not set!")
            raise ValueError("GitHub token is required")

        self._headers = {
            "Authorization": f"Bearer {self._token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }

        logger.debug(f"GitHub client initialized with base_url={base_url}")

    def _get(self, url: str, params: dict | None = None) -> dict:
        full_url = f"{self._base_url}{url}"
        logger.debug(f"GitHub API request: {full_url}, params={params}")

        response = requests.get(
            full_url,
            headers=self._headers,
            params=params
        )

        logger.debug(f"GitHub API response: {response.status_code}")

        if response.status_code == 401:
            raise Exception(
                "GitHub API authentication failed. Check your GITHUB_TOKEN. "
                "Make sure it's a valid Personal Access Token with 'public_repo' scope."
            )
        elif response.status_code == 403:
            raise Exception(
                "GitHub API rate limit exceeded or access forbidden. "
                "Wait a few minutes or check token permissions."
            )
        elif response.status_code == 404:
            raise Exception(
                f"Repository not found: {url}. Check owner and repo names."
            )
        elif response.status_code != 200:
            raise Exception(
                f"GitHub API error: {response.status_code} - {response.text}"
            )

        return response.json()

    def get_commits(self, owner: str, repo: str, since: str, until: str) -> list[dict]:
        params = {
            "since": since,
            "until": until,
            "per_page": 100
        }
        raw = self._get(f"/repos/{owner}/{repo}/commits", params=params)

        commits = []
        for commit in raw:
            try:
                commits.append({
                    "sha": commit["sha"],
                    "author": commit["commit"]["author"]["name"],
                    "message": commit["commit"]["message"],
                    "date": commit["commit"]["author"]["date"]
                })
            except KeyError as e:
                logger.warning(f"Skipping commit due to missing field: {e}")
                continue

        logger.info(f"Fetched {len(commits)} commits from {owner}/{repo}")
        return commits

    def get_issues(self, owner: str, repo: str) -> list[dict]:
        params = {
            "state": "open",
            "per_page": 20
        }
        raw = self._get(f"/repos/{owner}/{repo}/issues", params)

        issues = []
        for issue in raw:
            if "pull_request" not in issue:
                try:
                    issues.append({
                        "title": issue["title"],
                        "author": issue["user"]["login"],
                        "created_at": issue["created_at"],
                        "state": issue["state"],
                        "url": issue["html_url"]
                    })
                except KeyError as e:
                    logger.warning(f"Skipping issue due to missing field: {e}")
                    continue

        logger.info(f"Fetched {len(issues)} issues from {owner}/{repo}")
        return issues
