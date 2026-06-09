# Codebase Map

Generated: 2026-06-09T04:14:35Z | Files: 270 | Described: 0/270
<!-- gsd:codebase-meta {"generatedAt":"2026-06-09T04:14:35Z","fingerprint":"e05d01045ace34c31f983e8fa4eb327237a24f64","fileCount":270,"truncated":false} -->

### (root)/
- `.env.example`
- `.gitignore`
- `.pre-commit-config.yaml`
- `AGENTS.md`
- `CLAUDE.md`
- `docker-compose.yml`
- `GEMINI.md`
- `Makefile`
- `README.md`
- `skills-lock.json`

### .github/
- `.github/PULL_REQUEST_TEMPLATE.md`

### .github/agents/
- `.github/agents/backend-engineer.agent.md`
- `.github/agents/code-reviewer.agent.md`
- `.github/agents/docs-maintainer.agent.md`
- `.github/agents/frontend-engineer.agent.md`
- `.github/agents/report-pipeline-engineer.agent.md`
- `.github/agents/test-engineer.agent.md`

### .github/instructions/
- `.github/instructions/agent_maintenance_workflow.instructions.md`
- `.github/instructions/backend_app.instructions.md`
- `.github/instructions/code_writing_behavior.instructions.md`
- `.github/instructions/delegation_policy.instructions.md`
- `.github/instructions/frontend_app.instructions.md`
- `.github/instructions/frontend_quality_gates.instructions.md`
- `.github/instructions/python_quality_gates.instructions.md`
- `.github/instructions/qa_readonly.instructions.md`
- `.github/instructions/tests.instructions.md`

### .github/skills/backend-contract-check/
- `.github/skills/backend-contract-check/SKILL.md`

### .github/skills/frontend-linting/
- `.github/skills/frontend-linting/SKILL.md`

### .github/skills/frontend-testing/
- `.github/skills/frontend-testing/SKILL.md`

### .github/skills/python-linting/
- `.github/skills/python-linting/SKILL.md`

### .github/skills/python-testing/
- `.github/skills/python-testing/SKILL.md`

### .github/workflows/
- `.github/workflows/ci.yml`
- `.github/workflows/trigger_jules.yml`

### backend/
- `backend/.dockerignore`
- `backend/.env.example`
- `backend/Dockerfile`
- `backend/pyproject.toml`
- `backend/README.md`

### backend/app/
- `backend/app/__init__.py`
- `backend/app/config.py`
- `backend/app/main.py`
- `backend/app/schemas.py`

### backend/app/agent/
- `backend/app/agent/__init__.py`
- `backend/app/agent/checkpointer.py`
- `backend/app/agent/graph.py`
- `backend/app/agent/llm.py`
- `backend/app/agent/tools.py`

### backend/app/api/
- `backend/app/api/__init__.py`
- `backend/app/api/chat.py`
- `backend/app/api/finance.py`
- `backend/app/api/fusion.py`
- `backend/app/api/health.py`
- `backend/app/api/ingest.py`
- `backend/app/api/reports.py`
- `backend/app/api/threads.py`

### backend/app/kb/
- `backend/app/kb/__init__.py`
- `backend/app/kb/base.py`
- `backend/app/kb/fake.py`
- `backend/app/kb/memorypalace.py`

### backend/app/services/
- *(34 files: 34 .py)*

### backend/backend/data/
- `backend/backend/data/smoke-checkpoints.sqlite`
- `backend/backend/data/smoke-registry.sqlite`
- `backend/backend/data/smoke-report-sessions.sqlite`

### backend/tests/
- `backend/tests/__init__.py`
- `backend/tests/_fakes.py`
- `backend/tests/conftest.py`
- `backend/tests/test_fixtures.py`

### backend/tests/e2e/
- `backend/tests/e2e/__init__.py`
- `backend/tests/e2e/test_golden_demo_smoke.py`

### backend/tests/fixtures/flowdraft/
- `backend/tests/fixtures/flowdraft/demo_compliance_report.json`
- `backend/tests/fixtures/flowdraft/demo_datacentre.json`
- `backend/tests/fixtures/flowdraft/demo_floorplan.json`
- `backend/tests/fixtures/flowdraft/mock_graph.json`
- `backend/tests/fixtures/flowdraft/PROVENANCE.md`

### backend/tests/fixtures/graphs/
- `backend/tests/fixtures/graphs/architecture_only.json`
- `backend/tests/fixtures/graphs/fused_graph.json`
- `backend/tests/fixtures/graphs/mep_only.json`

### backend/tests/integration/
- `backend/tests/integration/__init__.py`
- `backend/tests/integration/test_app_state.py`
- `backend/tests/integration/test_chat_endpoint.py`
- `backend/tests/integration/test_demo_api.py`
- `backend/tests/integration/test_engineering_project_ingestion.py`
- `backend/tests/integration/test_health.py`
- `backend/tests/integration/test_ingest_endpoint.py`
- `backend/tests/integration/test_memorypalace_kb.py`
- `backend/tests/integration/test_report_full_path.py`
- `backend/tests/integration/test_reports_endpoint.py`
- `backend/tests/integration/test_thread_persistence.py`
- `backend/tests/integration/test_threads_api.py`

### backend/tests/unit/
- *(40 files: 40 .py)*

### backend/tests/unit/api/
- `backend/tests/unit/api/test_finance.py`

### backend/tests/unit/services/
- `backend/tests/unit/services/test_property_valuation.py`

### dataSamples/
- `dataSamples/schema.json`

### dc_compliance_checker/
- `dc_compliance_checker/.env.example`
- `dc_compliance_checker/.gitignore`
- `dc_compliance_checker/how_to_run.txt`
- `dc_compliance_checker/main.py`
- `dc_compliance_checker/requirements.txt`

### dc_compliance_checker/data/
- `dc_compliance_checker/data/sample_standard.txt`

### dc_compliance_checker/database/
- `dc_compliance_checker/database/__init__.py`
- `dc_compliance_checker/database/models.py`
- `dc_compliance_checker/database/setup.py`

### dc_compliance_checker/engine/
- `dc_compliance_checker/engine/__init__.py`
- `dc_compliance_checker/engine/rules.py`
- `dc_compliance_checker/engine/validator.py`

### dc_compliance_checker/parsers/
- `dc_compliance_checker/parsers/__init__.py`
- `dc_compliance_checker/parsers/dxf_parser.py`
- `dc_compliance_checker/parsers/graph_parser.py`
- `dc_compliance_checker/parsers/pdf_parser.py`
- `dc_compliance_checker/parsers/text_parser.py`

### docs/
- `docs/graph_artifact_persistence.md`
- `docs/graph_database_decision_record.md`
- `docs/plumbing_graph_taxonomy.md`
- `docs/standards_scraping_rules.md`

### frontend/
- `frontend/.dockerignore`
- `frontend/.env.example`
- `frontend/.eslintrc.json`
- `frontend/Dockerfile`
- `frontend/next-env.d.ts`
- `frontend/next.config.mjs`
- `frontend/package-lock.json`
- `frontend/package.json`
- `frontend/playwright.config.ts`
- `frontend/postcss.config.mjs`
- `frontend/README.md`
- `frontend/tailwind.config.ts`
- `frontend/tsconfig.json`
- `frontend/vitest.config.ts`

### frontend/public/
- `frontend/public/.gitkeep`

### frontend/src/app/
- `frontend/src/app/globals.css`
- `frontend/src/app/layout.tsx`
- `frontend/src/app/page.tsx`

### frontend/src/app/api/health/
- `frontend/src/app/api/health/route.ts`

### frontend/src/components/
- `frontend/src/components/ChatShell.tsx`
- `frontend/src/components/Composer.tsx`
- `frontend/src/components/ConnectionBadge.tsx`
- `frontend/src/components/Message.tsx`
- `frontend/src/components/MessageList.tsx`
- `frontend/src/components/ThreadList.tsx`
- `frontend/src/components/TypingIndicator.tsx`

### frontend/src/components/chat/
- `frontend/src/components/chat/ChatPanel.tsx`
- `frontend/src/components/chat/ReportCard.tsx`
- `frontend/src/components/chat/ReportGateForm.tsx`

### frontend/src/components/demo/
- `frontend/src/components/demo/ComplianceView.tsx`
- `frontend/src/components/demo/RoomsView.tsx`
- `frontend/src/components/demo/ValuationView.tsx`

### frontend/src/components/dock/
- `frontend/src/components/dock/BottomDock.tsx`

### frontend/src/components/files/
- `frontend/src/components/files/FileTree.tsx`

### frontend/src/components/graph/
- `frontend/src/components/graph/GraphView.tsx`

### frontend/src/components/onboarding/
- `frontend/src/components/onboarding/OnboardingWizard.tsx`

### frontend/src/components/preview/
- `frontend/src/components/preview/FilePreview.tsx`

### frontend/src/components/profile/
- `frontend/src/components/profile/ProfilePanel.tsx`

### frontend/src/components/report/
- `frontend/src/components/report/ReportView.tsx`

### frontend/src/components/settings/
- `frontend/src/components/settings/SettingsModal.tsx`

### frontend/src/components/shell/
- `frontend/src/components/shell/ActivityBar.tsx`
- `frontend/src/components/shell/AppShell.tsx`
- `frontend/src/components/shell/TopBar.tsx`

### frontend/src/lib/
- `frontend/src/lib/animations.ts`
- `frontend/src/lib/api.ts`
- `frontend/src/lib/mock.ts`
- `frontend/src/lib/store.ts`

### frontend/src/types/
- `frontend/src/types/index.ts`

### frontend/tests/
- `frontend/tests/setup.ts`

### frontend/tests/e2e/
- `frontend/tests/e2e/demo.spec.ts`
- `frontend/tests/e2e/pipeline.spec.ts`
- `frontend/tests/e2e/report.spec.ts`

### frontend/tests/fixtures/flowdraft/
- `frontend/tests/fixtures/flowdraft/demo_compliance_report.json`
- `frontend/tests/fixtures/flowdraft/demo_datacentre.json`
- `frontend/tests/fixtures/flowdraft/demo_floorplan.json`
- `frontend/tests/fixtures/flowdraft/mock_graph.json`
- `frontend/tests/fixtures/flowdraft/PROVENANCE.md`

### frontend/tests/fixtures/graphs/
- `frontend/tests/fixtures/graphs/architecture_only.json`
- `frontend/tests/fixtures/graphs/fused_graph.json`
- `frontend/tests/fixtures/graphs/mep_only.json`

### frontend/tests/unit/
- `frontend/tests/unit/api.test.ts`
- `frontend/tests/unit/Composer.test.tsx`
- `frontend/tests/unit/demo_workflow.test.tsx`
- `frontend/tests/unit/fixtures.test.ts`
- `frontend/tests/unit/hvac_types.test.ts`
- `frontend/tests/unit/Message.test.tsx`
- `frontend/tests/unit/ReportView.test.tsx`
- `frontend/tests/unit/store.test.ts`
- `frontend/tests/unit/test_flowdraft_fixtures.test.ts`

### frontend/tests/unit/flows/
- `frontend/tests/unit/flows/01-onboarding-step1.test.tsx`
- `frontend/tests/unit/flows/02-onboarding-step2.test.tsx`
- `frontend/tests/unit/flows/03-loading-to-shell.test.tsx`
- `frontend/tests/unit/flows/04-profile-export.test.tsx`
- `frontend/tests/unit/flows/05-settings-tabs.test.tsx`
- `frontend/tests/unit/flows/06-drop-creates-snapshot-and-warnings.test.tsx`
- `frontend/tests/unit/flows/07-snapshot-timeline.test.tsx`
- `frontend/tests/unit/flows/08-chat-citations-highlight-graph.test.tsx`
- `frontend/tests/unit/flows/09-snapshot-on-edit.test.tsx`
- `frontend/tests/unit/flows/10-build-report-and-gate.test.tsx`
- `frontend/tests/unit/flows/11-report-view-toggle.test.tsx`
- `frontend/tests/unit/flows/12-report-full-path.test.tsx`

### scripts/
- `scripts/gsd_task_bridge.py`
- `scripts/smoke_cad_converter.py`
- `scripts/smoke.sh`
