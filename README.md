Track: A
# GitHub Team Analytics Agent

AI-powered agent for analyzing GitHub repository activity. Built with pure Python, FastAPI, and OpenAI GPT-OSS-20B (free tier).

## Architecture
<pre>
├── src/services/github_client/
│ ├── agent/ # Agent core (Planner, Executor, Application)
│ ├── tools/ # Tools (CommitTool, IssueTool, DiffSummaryTool)
│ ├── domain/ # Business logic (AnalyticsService + protocols)
│ ├── adapters/ # External services (GitHub API, LLM)
│ ├── models/ # Data classes (Commit, Issue)
│ └── api/ # FastAPI router
└── frontend/ # Web UI
</pre>

**Agent Pipeline:**
User Query -> API Router -> Planner (LLM) -> [commits, issues, summary] -> Executor (Tools) -> GitHub API -> Analytics -> Final LLM Summary -> Response

## Quick Start

### Dependencies
- Python 3.11+
- uv
- OpenAI API key (free tier for gpt-oss-20b)
- Docker

### 1. Setup and Run

```bash
# Clone repository
git clone https://github.com/InchanterX/GitHub-Team-Analytics-Agent
cd GitHub-Team-Analytics-Agent

# Setup env
cp env.example .env
# Add your OpenAI API key to .env:
# OPENAI_API_KEY=your_key_here
# LLM_MODEL=gpt-oss-20b

# Install dependencies and run
uv sync && uv run python -m src.main run
```

## Web Interface
```bash
docker compose up --build
# Open http://localhost:3000
```