"""Standards indexing service for vector RAG."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from app.kb.base import KnowledgeBase
from app.schemas import StandardReviewState
from app.services.standards_catalog import get_standard

logger = logging.getLogger(__name__)


@dataclass
class StandardClause:
    source_id: str
    clause_id: str
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)


async def index_clause(kb: KnowledgeBase, clause: StandardClause) -> str | None:
    """Index a standard clause into the knowledge base if it has been reviewed.

    Returns the memory ID if successful, or None if the standard is not reviewed
    or not found.
    """
    standard = get_standard(clause.source_id)
    if not standard:
        logger.warning(f"Standard {clause.source_id} not found in catalog, skipping.")
        return None

    if standard.review_state != StandardReviewState.REVIEWED:
        logger.warning(f"Standard {clause.source_id} is not REVIEWED, skipping indexing.")
        return None

    # Construct the metadata dictionary
    version = None
    if standard.provenance:
        version = standard.provenance.hash_or_version

    metadata = {
        "source": clause.source_id,
        "jurisdiction": standard.jurisdiction,
        "discipline": standard.discipline,
        "clause": clause.clause_id,
        "version": version,
    }
    # Allow overriding or adding additional metadata
    metadata.update(clause.metadata)

    # Format the content with provenance
    fields = [
        f"source={clause.source_id}",
        f"jurisdiction={standard.jurisdiction}",
        f"discipline={standard.discipline}",
        f"clause={clause.clause_id}",
    ]
    if version:
        fields.append(f"version={version}")

    header = f"[{'; '.join(fields)}]"
    content = f"{header}\n{clause.text}"

    # Insert into KB
    memory_id = await kb.remember(content, metadata=metadata)
    return memory_id


# Sample fixture clauses
FIXTURE_CLAUSES = [
    StandardClause(
        source_id="gost-r-21-1101-2013",
        clause_id="5.2.1",
        text="The main set of working drawings includes general data on the working drawings.",
    ),
    StandardClause(
        source_id="gost-r-21-1101-2013",
        clause_id="5.2.2",
        text="Drawings of plans, sections and facades.",
    ),
    StandardClause(
        source_id="ibc-2021",
        clause_id="1004.5",
        text=(
            "Areas without fixed seating. The number of occupants shall be computed "
            "at the rate of one occupant per unit of area."
        ),
    ),
]


async def index_fixture_clauses(kb: KnowledgeBase) -> list[str]:
    """Iterate and index all fixture clauses into the given knowledge base."""
    memory_ids = []
    for clause in FIXTURE_CLAUSES:
        mid = await index_clause(kb, clause)
        if mid:
            memory_ids.append(mid)
    return memory_ids
