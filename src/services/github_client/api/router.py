from typing import Any
from fastapi import APIRouter, HTTPException, status
from src.services.github_client.agent.application import Agent
from datetime import datetime


def create_router(agent: Agent) -> APIRouter:
    router = APIRouter(prefix="/github", tags=["github"])

    @router.get("/analyze")
    async def analyze(query: str, owner: str, repo: str, since: str, until: str):
        try:
            if len(since) == 10:
                since = f"{since}T00:00:00Z"
            if len(until) == 10:
                until = f"{until}T23:59:59Z"

            datetime.fromisoformat(since.replace('Z', '+00:00'))
            datetime.fromisoformat(until.replace('Z', '+00:00'))
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid date format. Use YYYY-MM-DD or ISO 8601")

        params = {
            "owner": owner,
            "repo": repo,
            "since": since,
            "until": until
        }
        return agent.run(query, params)

    return router
