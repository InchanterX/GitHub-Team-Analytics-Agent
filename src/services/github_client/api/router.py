from typing import Any
from fastapi import APIRouter
from src.services.github_client.agent.application import Agent


def create_router(agent: Agent) -> APIRouter:
    router = APIRouter(prefix="/github", tags=["github"])

    @router.get("/analyze")
    async def analyze(query: str, owner: str, repo: str, since: str, until: str):
        params = {
            "owner": owner,
            "repo": repo,
            "since": since,
            "until": until
        }
        return agent.run(query, params)

    return router
