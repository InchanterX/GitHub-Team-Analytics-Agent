import asyncio

import typer
import uvicorn
import sys
import os
from fastapi import FastAPI
from loguru import logger
from src.services.github_client.api.router import create_router
from src.services.github_client.domain.analytics_service import AnalyticsService
from src.services.github_client.adapters.github.github_repository import GitHubRepositoryImplementation
from src.services.github_client.adapters.github.github_client import GitHubClient
from src.services.github_client.adapters.llm.openai_provider import OpenAIProvider
from src.services.github_client.agent.executor import Executor
from src.services.github_client.agent.planner import Planner
from src.services.github_client.agent.application import Agent
from src.services.github_client.settings import Settings


async def _run(settings: Settings) -> None:
    # Starting service itself with prepared submodules
    github_client = GitHubClient(
        base_url=os.getenv("GITHUB_API_URL"),
        token=os.getenv("GITHUB_TOKEN")
    )
    github_repo = GitHubRepositoryImplementation(github_client)
    llm = OpenAIProvider(
        api_key=os.getenv("LLM_API_KEY")
    )

    analytics_service = AnalyticsService(github_repo)
    executor = Executor(analytics_service)
    planner = Planner(llm)
    agent = Agent(planner, executor, llm)
    logger.debug("Analytics Service started")

    # Start Fastapi app and make it able to use all endpoints
    fastapi_app = FastAPI(title="Analytics Service")
    router = create_router(agent)
    fastapi_app.include_router(router)
    logger.debug("HTTP router registered")

    # Starting service of assembled app with prepared parameters using uvicorn
    config = uvicorn.Config(
        fastapi_app,
        host=settings.http_host,
        port=settings.http_port
    )
    server = uvicorn.Server(config)
    logger.info("Starting service on {}:{}",
                settings.http_host, settings.http_port)

    try:
        await asyncio.gather(server.serve())
    finally:
        logger.info("Shutdown complete")


app = typer.Typer()


def _setup_logger(settings: Settings) -> None:
    logger.remove()
    logger.add(
        sink=sys.stderr,
        level=settings.log_level.upper(),
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level:<8}</level> | <cyan>{name}</cyan>:<cyan>{line}</cyan> - {message}",
    )


@app.command()
def run() -> None:
    settings = Settings()
    _setup_logger(settings)
    logger.debug("Settings loaded: {}", settings.model_dump())
    asyncio.run(_run(settings))


if __name__ == "__main__":
    app()
