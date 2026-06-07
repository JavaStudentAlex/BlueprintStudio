# Standards Source Integration Rules

This document outlines the rules and procedures for integrating external standards, regulations, and codes into BlueprintStudio.

## General Principles
- Do not scrape live external standard sites directly from test or operational code without an explicit review.
- All standards data used for default development and tests must be mocked or represented by internal fixtures.
- Source catalog entries must provide full provenance including `retrieval_method`, `review_state`, and origin tracking.

## Scraping and Ingestion Rules
When configuring dynamic scraping or API pulls for standard source entries, the following policies apply:
1. **Respect `robots.txt`**: Automated retrievers must respect site crawl delay and allowed paths.
2. **Rate Limiting**: Retrievers must implement conservative rate limiting (e.g., 1 request per second) unless explicit API quotas dictate otherwise.
3. **Static vs. Dynamic Scraping**:
   - Favor manual PDF upload (`manual_pdf`) or official APIs (`api_pull`) when possible.
   - Fall back to static scraping (`static_scrape`) for HTML-based codes only when terms of service allow it.
   - Limit dynamic scraping (`dynamic_scrape`) requiring headless browsers to a last-resort approach, which must undergo explicit technical and legal review.

## Human Review Workflows
- **Pending Review**: A newly added standard source starts in a `pending` state. No automated downstream rule generation should execute on pending sources.
- **Review Criteria**: A human reviewer (or a separate review loop) must confirm the data quality, correctness of language/discipline classification, and license access before moving the source to `reviewed`.
- **Rejection/Deprecation**: Sources that are superseded by newer versions or fail quality checks should be marked as `deprecated` or `rejected`, leaving an audit trail in the registry.
