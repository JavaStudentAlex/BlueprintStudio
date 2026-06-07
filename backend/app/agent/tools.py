"""LangChain tools that expose the KnowledgeBase to the agent.

The KB is captured by closure so we can build a fresh tool list per request
backed by the same in-memory or Postgres-backed KB instance.
"""

from __future__ import annotations

import json

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from app.kb.base import KnowledgeBase
from app.services.graph_artifacts import GraphArtifactRegistry
from app.services.hybrid_retriever import HybridRetriever


class _RecallArgs(BaseModel):
    query: str = Field(description="Natural-language query to search the knowledge base.")
    k: int = Field(default=5, ge=1, le=20, description="Max number of memories to return.")


class _RememberArgs(BaseModel):
    content: str = Field(description="The fact, decision, or note to remember.")


def build_kb_tools(kb: KnowledgeBase) -> list[StructuredTool]:
    async def _recall(query: str, k: int = 5) -> str:
        hits = await kb.recall(query, k=k)
        if not hits:
            return "No relevant memories found."
        return "\n".join(f"- ({h['id']}) {h['content']}" for h in hits)

    async def _remember(content: str) -> str:
        mid = await kb.remember(content)
        return f"Remembered with id {mid}."

    return [
        StructuredTool.from_function(
            coroutine=_recall,
            name="kb_recall",
            description=(
                "Search the knowledge base for memories relevant to a query. "
                "Use this whenever the user asks about prior context, ingested "
                "documents, or facts that may already be stored."
            ),
            args_schema=_RecallArgs,
        ),
        StructuredTool.from_function(
            coroutine=_remember,
            name="kb_remember",
            description=(
                "Persist a new fact or decision to long-term memory. "
                "Use this when the user explicitly tells you to remember something."
            ),
            args_schema=_RememberArgs,
        ),
    ]


class _HybridRecallArgs(BaseModel):
    query: str = Field(description="Natural-language query to search for evidence.")
    document_id: str | None = Field(
        default=None, description="Optional document ID to restrict graph search."
    )
    project_id: str | None = Field(
        default=None, description="Optional project ID to restrict graph search."
    )
    k: int = Field(default=5, ge=1, le=20, description="Max number of text memories to return.")


def build_hybrid_kb_tools(
    kb: KnowledgeBase, registry: GraphArtifactRegistry
) -> list[StructuredTool]:
    retriever = HybridRetriever(kb, registry)

    async def _hybrid_recall(
        query: str, document_id: str | None = None, project_id: str | None = None, k: int = 5
    ) -> str:
        result = await retriever.retrieve(
            query, document_id=document_id, project_id=project_id, k_text=k
        )

        parts = []
        if result.text_evidence:
            parts.append("Text Evidence:")
            for h in result.text_evidence:
                parts.append(f"- ({h['id']}) {h['content']}")

        if result.graph_evidence:
            parts.append("Graph Evidence:")
            for ge in result.graph_evidence:
                parts.append(f"Artifact {ge.source_artifact_id}:")
                if ge.spaces:
                    parts.append(f"  Spaces: {json.dumps(ge.spaces)}")
                if ge.nodes:
                    parts.append(f"  Nodes: {json.dumps(ge.nodes)}")
                if ge.fixtures:
                    parts.append(f"  Fixtures: {json.dumps(ge.fixtures)}")
                if ge.edges:
                    parts.append(f"  Edges: {json.dumps(ge.edges)}")

        if not parts:
            return "No relevant text or graph evidence found."

        return "\n".join(parts)

    async def _remember(content: str) -> str:
        mid = await kb.remember(content)
        return f"Remembered with id {mid}."

    return [
        StructuredTool.from_function(
            coroutine=_hybrid_recall,
            name="hybrid_kb_recall",
            description=(
                "Search the knowledge base and engineering graph for memories relevant to a query. "
                "Use this whenever the user asks about prior context, ingested "
                "documents, or facts that may already be stored, combining text and "
                "structural evidence."
            ),
            args_schema=_HybridRecallArgs,
        ),
        StructuredTool.from_function(
            coroutine=_remember,
            name="kb_remember",
            description=(
                "Persist a new fact or decision to long-term memory. "
                "Use this when the user explicitly tells you to remember something."
            ),
            args_schema=_RememberArgs,
        ),
    ]
