import pytest

from app.agent.tools import build_kb_tools
from app.kb.fake import FakeKB
from app.schemas import (
    StandardLicenseStatus,
    StandardProvenance,
    StandardRetrievalMethod,
    StandardReviewState,
    StandardSourceCatalogEntry,
)
from app.services.standards_indexer import (
    StandardClause,
    index_clause,
    index_fixture_clauses,
)


# Mocking the `get_standard` import in standards_indexer to easily test missing/pending states
@pytest.fixture
def mock_catalog(monkeypatch):
    test_catalog = {
        "gost-r-21-1101-2013": StandardSourceCatalogEntry(
            source_id="gost-r-21-1101-2013",
            title="Test GOST",
            jurisdiction="Russian Federation",
            discipline="general",
            language="ru",
            license_status=StandardLicenseStatus.OPEN_ACCESS,
            retrieval_method=StandardRetrievalMethod.MANUAL_PDF,
            review_state=StandardReviewState.REVIEWED,
            provenance=StandardProvenance(
                source_name="Official GOST Protect Portal",
                hash_or_version="v2013",
            ),
        ),
        "pending-standard": StandardSourceCatalogEntry(
            source_id="pending-standard",
            title="Pending Standard",
            jurisdiction="USA",
            discipline="electrical",
            language="en",
            license_status=StandardLicenseStatus.OPEN_ACCESS,
            retrieval_method=StandardRetrievalMethod.MANUAL_PDF,
            review_state=StandardReviewState.PENDING,
            provenance=StandardProvenance(
                source_name="Test Source",
                hash_or_version="v1",
            ),
        ),
    }

    def mock_get_standard(source_id: str):
        return test_catalog.get(source_id)

    monkeypatch.setattr("app.services.standards_indexer.get_standard", mock_get_standard)
    return test_catalog


@pytest.mark.asyncio
async def test_index_clause_formats_correctly(mock_catalog):
    kb = FakeKB()
    clause = StandardClause(
        source_id="gost-r-21-1101-2013",
        clause_id="1.1",
        text="This is a test clause.",
    )
    mid = await index_clause(kb, clause)
    assert mid is not None

    records = kb.dump()
    assert len(records) == 1
    record = records[0]

    # Verify content formatting
    assert (
        "[source=gost-r-21-1101-2013; jurisdiction=Russian Federation; "
        "discipline=general; clause=1.1; version=v2013]"
    ) in record["content"]
    assert "This is a test clause." in record["content"]

    # Verify metadata
    assert record["metadata"]["source"] == "gost-r-21-1101-2013"
    assert record["metadata"]["jurisdiction"] == "Russian Federation"
    assert record["metadata"]["discipline"] == "general"
    assert record["metadata"]["clause"] == "1.1"
    assert record["metadata"]["version"] == "v2013"


@pytest.mark.asyncio
async def test_index_clause_rejects_unreviewed(mock_catalog):
    kb = FakeKB()
    clause = StandardClause(
        source_id="pending-standard",
        clause_id="2.1",
        text="This clause should not be indexed.",
    )
    mid = await index_clause(kb, clause)
    assert mid is None

    records = kb.dump()
    assert len(records) == 0


@pytest.mark.asyncio
async def test_index_clause_rejects_missing(mock_catalog):
    kb = FakeKB()
    clause = StandardClause(
        source_id="non-existent",
        clause_id="3.1",
        text="This clause should not be indexed.",
    )
    mid = await index_clause(kb, clause)
    assert mid is None

    records = kb.dump()
    assert len(records) == 0


@pytest.mark.asyncio
async def test_agent_can_retrieve_fixture_clauses():
    """Test using FakeKB directly and real FIXTURE_CLAUSES and standard_catalog."""
    kb = FakeKB()
    memory_ids = await index_fixture_clauses(kb)

    # Depending on how many reviewed standard clauses exist in the fixtures,
    # we assert some were indexed.
    # gost and ibc are REVIEWED in the real catalog.
    assert len(memory_ids) >= 2

    # Test retrieval via kb_recall tool
    tools = build_kb_tools(kb)
    kb_recall = next(t for t in tools if t.name == "kb_recall")

    result = await kb_recall.ainvoke({"query": "facades", "k": 5})
    assert "facades" in result.lower()
    assert "gost-r-21-1101-2013" in result
    assert "5.2.2" in result
