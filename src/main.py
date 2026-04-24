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
from src.services.github_client.adapters.llm.openai_client import OpenAIClient
from src.services.github_client.tools.github_commits import CommitTool
from src.services.github_client.tools.github_issues import IssueTool
from src.services.github_client.tools.github_diff_summary import DiffSummaryTool
from src.services.github_client.agent.executor import Executor
from src.services.github_client.agent.planner import Planner
from src.services.github_client.agent.application import Agent
from src.services.github_client.config import Settings


async def _run(settings: Settings) -> None:
    # Starting service itself with prepared submodules
    github_client = GitHubClient(
        base_url=os.getenv("GITHUB_API_URL", "https://api.github.com"),
        token=os.getenv("GITHUB_TOKEN")
    )
    github_repo = GitHubRepositoryImplementation(github_client)

    openai_client = OpenAIClient(
        api_key=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_API_URL"),
        model=os.getenv("LLM_MODEL", "gpt-4")
    )
    llm = OpenAIProvider(openai_client)

    analytics_service = AnalyticsService(github_repo)

    commit_tool = CommitTool(analytics_service)
    issue_tool = IssueTool(analytics_service)
    diff_summary_tool = DiffSummaryTool(llm)

    tools = {
        "commits": commit_tool,
        "issues": issue_tool,
        "summary": diff_summary_tool
    }

    executor = Executor(tools)
    planner = Planner(llm)
    agent = Agent(planner, executor, llm)
    logger.debug("Analytics Service started")

    # Start Fastapi app
    fastapi_app = FastAPI(title="Analytics Service")
    router = create_router(agent)
    fastapi_app.include_router(router)
    logger.debug("HTTP router registered")

    config = uvicorn.Config(
        fastapi_app,
        host=settings.http_host,
        port=settings.http_port
    )
    server = uvicorn.Server(config)
    logger.info("Starting service on {}:{}",
                settings.http_host, settings.http_port)

    try:
        await server.serve()
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
