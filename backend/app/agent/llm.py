"""LLM provider factory.

Selecting the chat LLM is a single source of truth so the rest of the agent
code never imports a concrete provider class. Switching providers is one env var.
"""

from __future__ import annotations

from typing import Any

from langchain_core.callbacks import AsyncCallbackManagerForLLMRun, CallbackManagerForLLMRun
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from app.config import Settings, get_settings


class FakeChatModel(BaseChatModel):
    """Deterministic local chat model for CI and offline smoke tests."""

    response: str = "Offline CI assistant response."

    @property
    def _llm_type(self) -> str:
        return "fake"

    def _message(self) -> AIMessage:
        return AIMessage(content=self.response)

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        return ChatResult(generations=[ChatGeneration(message=self._message())])

    async def _agenerate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: AsyncCallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        return ChatResult(generations=[ChatGeneration(message=self._message())])

    def bind_tools(self, tools: Any, **kwargs: Any):  # type: ignore[override]
        return self


def get_llm(settings: Settings | None = None) -> BaseChatModel:
    s = settings or get_settings()

    if s.llm_provider == "fake":
        return FakeChatModel()

    if s.llm_provider == "openai":
        if not s.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY is required when LLM_PROVIDER=openai. "
                "Set it in your environment or switch LLM_PROVIDER to 'ollama'."
            )
        return ChatOpenAI(
            model=s.openai_model,
            api_key=SecretStr(s.openai_api_key),
            temperature=0.2,
            streaming=True,
        )

    if s.llm_provider == "ollama":
        return ChatOllama(
            model=s.ollama_model,
            base_url=s.ollama_host,
            temperature=0.2,
        )

    raise ValueError(f"Unknown LLM_PROVIDER: {s.llm_provider!r}")
