import pytest

from app.schemas import (
    StandardLicenseStatus,
    StandardRetrievalMethod,
    StandardReviewState,
    StandardSourceCatalogEntry,
)
from app.services.standards_catalog import get_standard, list_standards


def test_standards_catalog_schema_validation():
    """Test that the StandardSourceCatalogEntry schema validates correctly."""
    entry = StandardSourceCatalogEntry(
        source_id="test-123",
        title="Test Standard",
        jurisdiction="Global",
        discipline="architecture",
        language="en",
        license_status=StandardLicenseStatus.OPEN_ACCESS,
        retrieval_method=StandardRetrievalMethod.API_PULL,
        review_state=StandardReviewState.REVIEWED,
    )
    assert entry.source_id == "test-123"
    assert entry.discipline == "architecture"

    with pytest.raises(ValueError):
        StandardSourceCatalogEntry(
            source_id="test-invalid",
            title="Invalid Standard",
            jurisdiction="Global",
            discipline="invalid_discipline",  # Should fail validation
            language="en",
            license_status=StandardLicenseStatus.OPEN_ACCESS,
            retrieval_method=StandardRetrievalMethod.API_PULL,
            review_state=StandardReviewState.REVIEWED,
        )


def test_fixture_standards_loaded():
    """Test that the fixture standards are available and correctly parsed."""
    standards = list_standards()
    assert len(standards) >= 3

    gost = get_standard("gost-r-21-1101-2013")
    assert gost is not None
    assert gost.title.startswith("GOST R 21.1101")
    assert gost.jurisdiction == "Russian Federation"
    assert gost.discipline == "general"
    assert gost.provenance is not None
    assert gost.provenance.source_name == "Official GOST Protect Portal"

    ibc = get_standard("ibc-2021")
    assert ibc is not None
    assert ibc.discipline == "architecture"
    assert ibc.license_status == StandardLicenseStatus.PAYWALL

    nec = get_standard("nec-2023")
    assert nec is not None
    assert nec.discipline == "electrical"
    assert nec.review_state == StandardReviewState.PENDING
