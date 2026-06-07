from app.schemas import (
    StandardLicenseStatus,
    StandardProvenance,
    StandardRetrievalMethod,
    StandardReviewState,
    StandardSourceCatalogEntry,
)

FIXTURE_STANDARDS: dict[str, StandardSourceCatalogEntry] = {
    "gost-r-21-1101-2013": StandardSourceCatalogEntry(
        source_id="gost-r-21-1101-2013",
        title=(
            "GOST R 21.1101-2013 System of project documents for construction. "
            "Main requirements for project and working documents"
        ),
        official_url="https://protect.gost.ru/document.aspx?control=7&id=184918",
        jurisdiction="Russian Federation",
        discipline="general",
        language="ru",
        license_status=StandardLicenseStatus.OPEN_ACCESS,
        retrieval_method=StandardRetrievalMethod.MANUAL_PDF,
        review_state=StandardReviewState.REVIEWED,
        provenance=StandardProvenance(
            source_name="Official GOST Protect Portal",
            last_retrieved_at="2023-10-25T10:00:00Z",
            hash_or_version="v2013",
            retriever_agent="human",
        ),
    ),
    "ibc-2021": StandardSourceCatalogEntry(
        source_id="ibc-2021",
        title="2021 International Building Code (IBC)",
        official_url="https://codes.iccsafe.org/content/IBC2021P2",
        jurisdiction="International/USA",
        discipline="architecture",
        language="en",
        license_status=StandardLicenseStatus.PAYWALL,
        retrieval_method=StandardRetrievalMethod.API_PULL,
        review_state=StandardReviewState.REVIEWED,
        provenance=StandardProvenance(
            source_name="ICC Premium Access API",
            last_retrieved_at="2023-11-01T12:00:00Z",
            hash_or_version="2021-edition",
            retriever_agent="sync_script",
        ),
    ),
    "nec-2023": StandardSourceCatalogEntry(
        source_id="nec-2023",
        title="NFPA 70, National Electrical Code (NEC)",
        official_url="https://www.nfpa.org/codes-and-standards/all-codes-and-standards/list-of-codes-and-standards/detail?code=70",
        jurisdiction="USA",
        discipline="electrical",
        language="en",
        license_status=StandardLicenseStatus.PAYWALL,
        retrieval_method=StandardRetrievalMethod.MANUAL_PDF,
        review_state=StandardReviewState.PENDING,
        provenance=StandardProvenance(
            source_name="NFPA Handbooks",
            last_retrieved_at="2023-11-15T09:30:00Z",
            hash_or_version="2023-edition",
            retriever_agent="human",
        ),
    ),
}


def get_standard(source_id: str) -> StandardSourceCatalogEntry | None:
    """Retrieve a standard source entry by its ID."""
    return FIXTURE_STANDARDS.get(source_id)


def list_standards() -> list[StandardSourceCatalogEntry]:
    """List all registered standard source entries."""
    return list(FIXTURE_STANDARDS.values())
