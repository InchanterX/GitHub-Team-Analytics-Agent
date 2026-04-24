from src.services.github_client.domain.protocols.llm_provider import LLMProvider


class DiffSummaryTool:
    def __init__(self, llm: LLMProvider):
        self._llm = llm

    def run(self, params: dict) -> str:
        prompt = f"""
        Summarize the changes made in the following commits:
        {params["commit_messages"]}
        """
        return self._llm.generate_response(prompt)
