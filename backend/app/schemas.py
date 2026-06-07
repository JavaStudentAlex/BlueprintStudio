"""Public API schemas shared between routes, the agent, and the frontend.

These are the wire format. Treat changes here as breaking.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

Role = Literal["user", "assistant", "system", "tool"]
ChunkType = Literal[
    "token",
    "tool_call",
    "tool_result",
    "error",
    "done",
    "report_card",
    "report_gate",
]
ReportSessionStatus = Literal["pending", "active", "blocked", "complete", "failed"]
ReportStageStatus = Literal["pending", "active", "complete", "failed"]
ReportGateStatus = Literal["open", "closed"]
ReportArtifactKind = Literal[
    "source_inventory_snapshot",
    "section_plan",
    "paragraph_citations",
    "validation_finding",
    "pdf_export",
    "other",
]
ReportCardKind = Literal[
    "stage_started",
    "stage_completed",
    "stage_failed",
    "gate_opened",
    "gate_closed",
    "failure",
]
ReportLogLevel = Literal["debug", "info", "warning", "error"]
ReportValidationSeverity = Literal["info", "warning", "blocker"]
ReportExportStatus = Literal["pending", "ready", "failed"]


def _coerce_json_object(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    return value


class Message(BaseModel):
    role: Role
    content: str = ""


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    thread_id: str | None = None

    @field_validator("message")
    @classmethod
    def _no_whitespace_only(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("message must not be whitespace only")
        return v


class ChatChunk(BaseModel):
    """One frame of an SSE stream."""

    type: ChunkType
    data: str = ""
    payload: dict[str, Any] = Field(default_factory=dict)

    @field_validator("payload", mode="before")
    @classmethod
    def _payload_defaults_to_empty_dict(cls, value: Any) -> dict[str, Any]:
        return _coerce_json_object(value)


class ThreadInfo(BaseModel):
    thread_id: str
    message_count: int = 0
    last_message_at: float | None = None


class ThreadHistory(BaseModel):
    thread_id: str
    messages: list[Message] = Field(default_factory=list)


class ThreadCreated(BaseModel):
    thread_id: str


class HealthStatus(BaseModel):
    status: Literal["ok"] = "ok"


class ReadinessStatus(BaseModel):
    status: Literal["ready", "degraded"]
    ollama: bool
    postgres: bool
    checkpointer: bool
    kb: bool
    detail: str | None = None


class IngestResponse(BaseModel):
    ingested_files: int
    ingested_chunks: int
    memory_ids: list[str] = Field(default_factory=list)


class ReportCardPayload(BaseModel):
    session_id: str
    stage_id: str
    stage_name: str
    kind: ReportCardKind
    message: str
    created_at: str
    payload: dict[str, Any] = Field(default_factory=dict)

    @field_validator("payload", mode="before")
    @classmethod
    def _payload_defaults_to_empty_dict(cls, value: Any) -> dict[str, Any]:
        return _coerce_json_object(value)


class ReportGatePayload(BaseModel):
    session_id: str
    gate_id: str
    stage_id: str | None = None
    question: dict[str, Any] = Field(default_factory=dict)
    status: ReportGateStatus
    created_at: str

    @field_validator("question", mode="before")
    @classmethod
    def _question_defaults_to_empty_dict(cls, value: Any) -> dict[str, Any]:
        return _coerce_json_object(value)


class ReportSessionLaunchRequest(BaseModel):
    session_id: str | None = None
    thread_id: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("metadata", mode="before")
    @classmethod
    def _metadata_defaults_to_empty_dict(cls, value: Any) -> dict[str, Any]:
        return _coerce_json_object(value)


class ReportSessionLaunchResponse(BaseModel):
    session_id: str
    status: ReportSessionStatus
    current_stage: str | None = None
    resumed: bool


class ReportGateAnswerRequest(BaseModel):
    answer: dict[str, Any]


class ReportSessionInspectionResponse(BaseModel):
    session: ReportSession
    current_stage: str | None = None
    stages: list[ReportStage] = Field(default_factory=list)
    gates: list[ReportGate] = Field(default_factory=list)
    artifacts: list[ReportArtifact] = Field(default_factory=list)
    validation_findings: list[ReportValidationFinding] = Field(default_factory=list)
    exports: list[ReportExport] = Field(default_factory=list)
    recent_logs: list[ReportLog] = Field(default_factory=list)


class ReportSession(BaseModel):
    session_id: str
    status: ReportSessionStatus = "pending"
    current_stage: str | None = None
    created_at: str
    updated_at: str | None = None
    last_error: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("metadata", mode="before")
    @classmethod
    def _metadata_defaults_to_empty_dict(cls, value: Any) -> dict[str, Any]:
        return _coerce_json_object(value)


class ReportStage(BaseModel):
    stage_id: str
    session_id: str
    name: str
    status: ReportStageStatus = "pending"
    started_at: str | None = None
    completed_at: str | None = None
    summary: str | None = None
    error: str | None = None


class ReportGate(BaseModel):
    gate_id: str
    session_id: str
    stage_id: str | None = None
    status: ReportGateStatus = "open"
    question: dict[str, Any] = Field(default_factory=dict)
    answer: dict[str, Any] = Field(default_factory=dict)
    created_at: str
    closed_at: str | None = None

    @field_validator("question", "answer", mode="before")
    @classmethod
    def _json_payload_defaults_to_empty_dict(cls, value: Any) -> dict[str, Any]:
        return _coerce_json_object(value)


class ReportArtifact(BaseModel):
    artifact_id: str
    session_id: str
    stage_id: str | None = None
    kind: ReportArtifactKind
    content: dict[str, Any]
    created_at: str

    @field_validator("content", mode="before")
    @classmethod
    def _content_defaults_to_empty_dict(cls, value: Any) -> dict[str, Any]:
        return _coerce_json_object(value)


class ReportLog(BaseModel):
    log_id: str
    session_id: str
    stage_id: str | None = None
    level: ReportLogLevel
    message: str
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: str

    @field_validator("payload", mode="before")
    @classmethod
    def _payload_defaults_to_empty_dict(cls, value: Any) -> dict[str, Any]:
        return _coerce_json_object(value)


class ReportValidationFinding(BaseModel):
    finding_id: str
    session_id: str
    severity: ReportValidationSeverity
    code: str | None = None
    message: str
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: str

    @field_validator("payload", mode="before")
    @classmethod
    def _payload_defaults_to_empty_dict(cls, value: Any) -> dict[str, Any]:
        return _coerce_json_object(value)


class ReportExport(BaseModel):
    export_id: str
    session_id: str
    status: ReportExportStatus = "pending"
    format: str
    output_path: str | None = None
    diagnostics: dict[str, Any] = Field(default_factory=dict)
    created_at: str
    completed_at: str | None = None

    @field_validator("diagnostics", mode="before")
    @classmethod
    def _diagnostics_defaults_to_empty_dict(cls, value: Any) -> dict[str, Any]:
        return _coerce_json_object(value)


class ErrorResponse(BaseModel):
    error: str
    detail: str | None = None


Discipline = Literal["architecture", "electrical", "plumbing", "hvac", "ventilation", "general"]


class GraphProvenance(BaseModel):
    model_config = ConfigDict(extra="forbid")
    source_file: str | None = None
    page_number: int | None = None
    parser_engine: str | None = None
    confidence: float | None = None


class GraphMeta(BaseModel):
    model_config = ConfigDict(extra="forbid")
    diagram_id: str | None = None
    diagram_type: str | None = None
    building_id: str | None = None
    scale: float | None = None
    title: str | None = None
    properties: dict[str, Any] = Field(default_factory=dict)

    @field_validator("properties", mode="before")
    @classmethod
    def _properties_defaults_to_empty_dict(cls, value: Any) -> dict[str, Any]:
        return _coerce_json_object(value)


class GraphSpace(BaseModel):
    model_config = ConfigDict(extra="forbid")
    space_id: str
    discipline: Discipline = "architecture"
    category: str | None = None
    polygon: list[list[float]] | None = None
    area: float | None = None
    floor: str | None = None
    properties: dict[str, Any] = Field(default_factory=dict)
    provenance: GraphProvenance | None = None

    @field_validator("properties", mode="before")
    @classmethod
    def _properties_defaults_to_empty_dict(cls, value: Any) -> dict[str, Any]:
        return _coerce_json_object(value)


class GraphWall(BaseModel):
    model_config = ConfigDict(extra="forbid")
    wall_id: str
    discipline: Discipline = "architecture"
    polyline: list[list[float]] | None = None
    properties: dict[str, Any] = Field(default_factory=dict)
    provenance: GraphProvenance | None = None

    @field_validator("properties", mode="before")
    @classmethod
    def _properties_defaults_to_empty_dict(cls, value: Any) -> dict[str, Any]:
        return _coerce_json_object(value)


class GraphFixture(BaseModel):
    model_config = ConfigDict(extra="forbid")
    fixture_id: str
    discipline: Discipline = "architecture"
    category: str | None = None
    position: list[float] | None = None
    space_id: str | None = None
    properties: dict[str, Any] = Field(default_factory=dict)
    provenance: GraphProvenance | None = None

    @field_validator("properties", mode="before")
    @classmethod
    def _properties_defaults_to_empty_dict(cls, value: Any) -> dict[str, Any]:
        return _coerce_json_object(value)


class GraphNode(BaseModel):
    model_config = ConfigDict(extra="forbid")
    node_id: str
    discipline: Discipline = "general"
    category: str | None = None
    position: list[float] | None = None
    space_id: str | None = None
    properties: dict[str, Any] = Field(default_factory=dict)
    provenance: GraphProvenance | None = None

    @field_validator("properties", mode="before")
    @classmethod
    def _properties_defaults_to_empty_dict(cls, value: Any) -> dict[str, Any]:
        return _coerce_json_object(value)


class GraphEdge(BaseModel):
    model_config = ConfigDict(extra="forbid")
    edge_id: str
    discipline: Discipline = "general"
    category: str | None = None
    source_id: str
    target_id: str
    polyline: list[list[float]] | None = None
    properties: dict[str, Any] = Field(default_factory=dict)
    provenance: GraphProvenance | None = None

    @field_validator("properties", mode="before")
    @classmethod
    def _properties_defaults_to_empty_dict(cls, value: Any) -> dict[str, Any]:
        return _coerce_json_object(value)


class GraphAnnotation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    annotation_id: str
    discipline: Discipline = "general"
    text: str
    position: list[float] | None = None
    properties: dict[str, Any] = Field(default_factory=dict)
    provenance: GraphProvenance | None = None

    @field_validator("properties", mode="before")
    @classmethod
    def _properties_defaults_to_empty_dict(cls, value: Any) -> dict[str, Any]:
        return _coerce_json_object(value)


class GraphValidationError(BaseModel):
    path: str
    code: str
    message: str
    severity: Literal["error", "warning"] = "error"


class EngineeringGraph(BaseModel):
    model_config = ConfigDict(extra="forbid")

    meta: GraphMeta = Field(default_factory=GraphMeta)
    spaces: list[GraphSpace] = Field(default_factory=list)
    walls: list[GraphWall] = Field(default_factory=list)
    fixtures: list[GraphFixture] = Field(default_factory=list)
    nodes: list[GraphNode] = Field(default_factory=list)
    edges: list[GraphEdge] = Field(default_factory=list)
    annotations: list[GraphAnnotation] = Field(default_factory=list)


class FuseRequest(BaseModel):
    architecture: EngineeringGraph
    mep: EngineeringGraph


class FuseResponse(BaseModel):
    fused_graph: EngineeringGraph
    warnings: list[str] = Field(default_factory=list)


class BreakerAnalysisResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    node_id: str
    tag: str | None = None
    downstream_load_kW: float  # noqa: N815
    computed_amps: float
    ampacity_A: float | None = None  # noqa: N815
    threshold: float
    status: Literal["OK", "OVERLOAD", "NO_RATING", "UNKNOWN"]
    reason: str | None = None


class ElectricalLoadAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")
    breakers: list[BreakerAnalysisResult] = Field(default_factory=list)


class HVACEquipmentRule(BaseModel):
    model_config = ConfigDict(extra="forbid")
    equipment_id: str
    rule_name: str
    expected: str
    actual: str
    passed: bool


class PUEAnalysisResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    total_facility_power_kW: float  # noqa: N815
    total_it_power_kW: float  # noqa: N815
    pue: float
    equipment_rules_passed: int
    equipment_rules_failed: int
    equipment_rules: list[HVACEquipmentRule] = Field(default_factory=list)


class StandardReviewState(StrEnum):
    PENDING = "pending"
    REVIEWED = "reviewed"
    REJECTED = "rejected"
    DEPRECATED = "deprecated"


class StandardRetrievalMethod(StrEnum):
    MANUAL_PDF = "manual_pdf"
    API_PULL = "api_pull"
    STATIC_SCRAPE = "static_scrape"
    DYNAMIC_SCRAPE = "dynamic_scrape"


class StandardLicenseStatus(StrEnum):
    OPEN_ACCESS = "open_access"
    PAYWALL = "paywall"
    INTERNAL_ONLY = "internal_only"


class StandardProvenance(BaseModel):
    model_config = ConfigDict(extra="forbid")
    source_name: str
    last_retrieved_at: str | None = None
    hash_or_version: str | None = None
    retriever_agent: str | None = None


class StandardSourceCatalogEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")
    source_id: str
    title: str
    official_url: str | None = None
    jurisdiction: str
    discipline: Discipline
    language: str
    license_status: StandardLicenseStatus
    retrieval_method: StandardRetrievalMethod
    review_state: StandardReviewState
    provenance: StandardProvenance | None = None


class ComplianceTargetClass(StrEnum):
    ROOM = "Room"
    AISLE = "Aisle"
    RACK = "Rack"
    EQUIPMENT = "Equipment"
    BUILDING = "Building"
    ANY = "Any"


class ComplianceCondition(StrEnum):
    MIN_WIDTH = "min_width"
    MAX_WIDTH = "max_width"
    MIN_AREA = "min_area"
    MIN_CLEARANCE = "min_clearance"
    MIN_POWER = "min_power"
    MAX_PUE = "max_pue"
    MUST_CONNECT_TO = "must_connect_to"
    MUST_EXIST = "must_exist"


class ComplianceRule(BaseModel):
    model_config = ConfigDict(use_enum_values=True, extra="forbid")

    target_class: ComplianceTargetClass
    target_type: str | None = None
    condition: ComplianceCondition
    value: float | str
    unit: str | None = None
    description: str | None = None
    source: str | None = None

    @field_validator("value", mode="before")
    @classmethod
    def _coerce_value(cls, v: Any) -> float | str:
        if isinstance(v, (int, float)):
            return float(v)
        s = str(v).strip()
        try:
            return float(s)
        except ValueError:
            return s


class ComplianceGeometryObject(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    id: str
    cls: ComplianceTargetClass = Field(alias="class")
    type: str | None = None
    geometry: Any = None
    calculated_metrics: dict[str, float] = Field(default_factory=dict)
    links: list[str] = Field(default_factory=list)


class ComplianceViolation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    rule: ComplianceRule
    target_object: str | None = None
    actual: float | str | None = None
    expected: float | str | None = None
    message: str
    severity: Literal["info", "warning", "error", "blocker"] = "error"
    source: str | None = None


class ComplianceValidationReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    violations: list[ComplianceViolation] = Field(default_factory=list)
    checks_run: int = 0

    @property
    def passed(self) -> bool:
        return len(self.violations) == 0
