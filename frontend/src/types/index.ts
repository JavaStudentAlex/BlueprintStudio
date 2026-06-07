export type JsonObject = Record<string, unknown>;

export type Role = "user" | "assistant" | "system" | "tool";

export type Message = {
  id: string;
  role: Role;
  content: string;
  pending?: boolean;
};

export type ReportSessionStatus =
  | "pending"
  | "active"
  | "blocked"
  | "complete"
  | "failed";

export type ReportStageStatus = "pending" | "active" | "complete" | "failed";

export type ReportGateStatus = "open" | "closed";

export type ReportCardKind =
  | "stage_started"
  | "stage_completed"
  | "stage_failed"
  | "gate_opened"
  | "gate_closed"
  | "failure";

export type ReportArtifactKind =
  | "source_inventory_snapshot"
  | "section_plan"
  | "section_draft"
  | "paragraph_citations"
  | "validation_finding"
  | "pdf_export"
  | "other";

export type ReportValidationSeverity = "info" | "warning" | "blocker";

export type ReportExportStatus = "pending" | "ready" | "failed";

export type ReportLogLevel = "debug" | "info" | "warning" | "error";

export type ReportArtifact = {
  artifact_id: string;
  session_id: string;
  stage_id: string | null;
  kind: ReportArtifactKind;
  content: JsonObject;
  created_at: string;
};

export type ReportValidationFinding = {
  finding_id: string;
  session_id: string;
  severity: ReportValidationSeverity;
  code: string | null;
  message: string;
  payload: JsonObject;
  created_at: string;
};

export type ReportExport = {
  export_id: string;
  session_id: string;
  status: ReportExportStatus;
  format: string;
  output_path: string | null;
  diagnostics: JsonObject;
  created_at: string;
  completed_at: string | null;
};


export type ReportCardPayload = {
  session_id: string;
  stage_id: string;
  stage_name: string;
  kind: ReportCardKind;
  message: string;
  created_at: string;
  payload: JsonObject;
};

export type ReportGatePayload = {
  session_id: string;
  gate_id: string;
  stage_id: string | null;
  question: JsonObject;
  status: ReportGateStatus;
  created_at: string;
};

export type ReportSessionLaunchRequest = {
  session_id?: string | null;
  thread_id?: string | null;
  metadata?: JsonObject;
};

export type ReportSessionLaunchResponse = {
  session_id: string;
  status: ReportSessionStatus;
  current_stage: string | null;
  resumed: boolean;
};

export type ReportSession = {
  session_id: string;
  status: ReportSessionStatus;
  current_stage: string | null;
  created_at: string;
  updated_at: string | null;
  last_error: string | null;
  metadata: JsonObject;
};

export type ReportStage = {
  stage_id: string;
  session_id: string;
  name: string;
  status: ReportStageStatus;
  started_at: string | null;
  completed_at: string | null;
  summary: string | null;
  error: string | null;
};

export type ReportGate = {
  gate_id: string;
  session_id: string;
  stage_id: string | null;
  status: ReportGateStatus;
  question: JsonObject;
  answer: JsonObject;
  created_at: string;
  closed_at: string | null;
};

export type ReportLog = {
  log_id: string;
  session_id: string;
  stage_id: string | null;
  level: ReportLogLevel;
  message: string;
  payload: JsonObject;
  created_at: string;
};

export type ReportSessionInspectionResponse = {
  session: ReportSession;
  current_stage: string | null;
  stages: ReportStage[];
  gates: ReportGate[];
  artifacts: ReportArtifact[];
  validation_findings: ReportValidationFinding[];
  exports: ReportExport[];
  recent_logs: ReportLog[];
};

export type ReportChatItem =
  | { itemType: "message"; message: Message }
  | { itemType: "report_card"; payload: ReportCardPayload }
  | { itemType: "report_gate"; payload: ReportGatePayload };

export type ChatChunk =
  | { type: "token"; data: string; payload?: JsonObject }
  | { type: "tool_call"; data: string; payload?: JsonObject }
  | { type: "tool_result"; data: string; payload?: JsonObject }
  | { type: "error"; data: string; payload?: JsonObject }
  | { type: "done"; data: string; payload?: JsonObject }
  | { type: "report_card"; data: string; payload: ReportCardPayload }
  | { type: "report_gate"; data: string; payload: ReportGatePayload };

export type ThreadInfo = {
  thread_id: string;
  message_count: number;
  last_message_at: number | null;
};

export type ThreadHistory = {
  thread_id: string;
  messages: { role: Role; content: string }[];
};

export type Health = { status: "ok" };

export type Readiness = {
  status: "ready" | "degraded";
  ollama: boolean;
  postgres: boolean;
  checkpointer: boolean;
  kb: boolean;
  detail: string | null;
};


export type Discipline = "architecture" | "electrical" | "plumbing" | "hvac" | "ventilation" | "general";

export type GraphProvenance = {
  source_file: string | null;
  page_number: number | null;
  parser_engine: string | null;
  confidence: number | null;
};

export type GraphMeta = {
  diagram_id: string | null;
  diagram_type: string | null;
  building_id: string | null;
  scale: number | null;
  title: string | null;
  properties: JsonObject;
};

export type GraphSpace = {
  space_id: string;
  discipline: Discipline;
  category: string | null;
  polygon: number[][] | null;
  area: number | null;
  floor: string | null;
  properties: JsonObject;
  provenance: GraphProvenance | null;
};

export type GraphWall = {
  wall_id: string;
  discipline: Discipline;
  polyline: number[][] | null;
  properties: JsonObject;
  provenance: GraphProvenance | null;
};

export type GraphFixture = {
  fixture_id: string;
  discipline: Discipline;
  category: string | null;
  position: number[] | null;
  space_id: string | null;
  properties: JsonObject;
  provenance: GraphProvenance | null;
};

export type GraphNode = {
  node_id: string;
  discipline: Discipline;
  category: string | null;
  position: number[] | null;
  space_id: string | null;
  properties: JsonObject;
  provenance: GraphProvenance | null;
};

export type GraphEdge = {
  edge_id: string;
  discipline: Discipline;
  category: string | null;
  source_id: string;
  target_id: string;
  polyline: number[][] | null;
  properties: JsonObject;
  provenance: GraphProvenance | null;
};

export type GraphAnnotation = {
  annotation_id: string;
  discipline: Discipline;
  text: string;
  position: number[] | null;
  properties: JsonObject;
  provenance: GraphProvenance | null;
};

export type EngineeringGraph = {
  meta: GraphMeta;
  spaces: GraphSpace[];
  walls: GraphWall[];
  fixtures: GraphFixture[];
  nodes: GraphNode[];
  edges: GraphEdge[];
  annotations: GraphAnnotation[];
};

export type FuseRequest = {
  architecture: EngineeringGraph;
  mep: EngineeringGraph;
};

export type FuseResponse = {
  fused_graph: EngineeringGraph;
  warnings: string[];
};
