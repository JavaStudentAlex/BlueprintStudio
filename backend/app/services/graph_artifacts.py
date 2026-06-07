"""Persistence layer for parsed engineering graph artifacts."""

import json
import os
import sqlite3
import threading
import uuid
from collections.abc import AsyncIterator, Sequence
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from app.schemas import EngineeringGraph


@dataclass(frozen=True, slots=True)
class GraphArtifactRecord:
    """A durable record of a parsed engineering graph."""

    artifact_id: str
    document_id: str | None
    project_id: str | None
    schema_version: str
    graph_data: EngineeringGraph
    created_at: str


class GraphArtifactRegistry:
    """Stores parsed engineering graphs in a private SQLite database."""

    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn
        self._conn.row_factory = sqlite3.Row
        self._lock = threading.RLock()
        self._ensure_schema()

    def store_artifact(
        self,
        graph: EngineeringGraph,
        *,
        document_id: str | None = None,
        project_id: str | None = None,
        schema_version: str = "1.0",
        artifact_id: str | None = None,
    ) -> GraphArtifactRecord:
        """Store an EngineeringGraph as a durable JSON artifact."""
        if document_id is None and project_id is None:
            raise ValueError("must provide either document_id or project_id")

        candidate_id = (artifact_id or uuid.uuid4().hex).strip()
        timestamp = datetime.now(UTC).isoformat()
        graph_json = graph.model_dump_json(exclude_none=True)

        with self._lock:
            with self._conn:
                self._conn.execute(
                    """
                    INSERT INTO graph_artifacts (
                        artifact_id,
                        document_id,
                        project_id,
                        schema_version,
                        graph_data,
                        created_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        candidate_id,
                        document_id,
                        project_id,
                        schema_version,
                        graph_json,
                        timestamp,
                    ),
                )

            record = self.get_by_id(candidate_id)
            if record is None:
                raise RuntimeError("graph artifact insert did not produce a row")
            return record

    def get_by_id(self, artifact_id: str) -> GraphArtifactRecord | None:
        """Return a graph artifact by its ID."""
        with self._lock:
            row = self._conn.execute(
                """
                SELECT artifact_id, document_id, project_id, schema_version, graph_data, created_at
                FROM graph_artifacts
                WHERE artifact_id = ?
                """,
                (artifact_id,),
            ).fetchone()
        return self._row_to_record(row) if row is not None else None

    def get_by_document_id(self, document_id: str) -> Sequence[GraphArtifactRecord]:
        """Return all graph artifacts for a document, ordered newest first."""
        with self._lock:
            rows = self._conn.execute(
                """
                SELECT artifact_id, document_id, project_id, schema_version, graph_data, created_at
                FROM graph_artifacts
                WHERE document_id = ?
                ORDER BY created_at DESC, artifact_id ASC
                """,
                (document_id,),
            ).fetchall()
        return [self._row_to_record(row) for row in rows]

    def get_by_project_id(self, project_id: str) -> Sequence[GraphArtifactRecord]:
        """Return all graph artifacts for a project, ordered newest first."""
        with self._lock:
            rows = self._conn.execute(
                """
                SELECT artifact_id, document_id, project_id, schema_version, graph_data, created_at
                FROM graph_artifacts
                WHERE project_id = ?
                ORDER BY created_at DESC, artifact_id ASC
                """,
                (project_id,),
            ).fetchall()
        return [self._row_to_record(row) for row in rows]

    def close(self) -> None:
        """Close the underlying SQLite connection."""
        with self._lock:
            self._conn.close()

    def _ensure_schema(self) -> None:
        with self._lock:
            with self._conn:
                self._conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS graph_artifacts (
                        artifact_id TEXT PRIMARY KEY,
                        document_id TEXT,
                        project_id TEXT,
                        schema_version TEXT NOT NULL,
                        graph_data TEXT NOT NULL,
                        created_at TEXT NOT NULL
                    )
                    """
                )
                self._conn.execute(
                    """
                    CREATE INDEX IF NOT EXISTS idx_graph_artifacts_document_id
                    ON graph_artifacts(document_id)
                    """
                )
                self._conn.execute(
                    """
                    CREATE INDEX IF NOT EXISTS idx_graph_artifacts_project_id
                    ON graph_artifacts(project_id)
                    """
                )

    def _row_to_record(self, row: sqlite3.Row) -> GraphArtifactRecord:
        raw_data = json.loads(row["graph_data"])
        graph = EngineeringGraph.model_validate(raw_data)

        return GraphArtifactRecord(
            artifact_id=row["artifact_id"],
            document_id=row["document_id"],
            project_id=row["project_id"],
            schema_version=row["schema_version"],
            graph_data=graph,
            created_at=row["created_at"],
        )


@asynccontextmanager
async def lifespan_graph_artifacts(
    db_path: str | Path,
) -> AsyncIterator[GraphArtifactRegistry]:
    """Open the graph artifact registry for the lifetime of the app."""
    path = str(db_path)
    if path != ":memory:":
        parent = os.path.dirname(os.path.abspath(path))
        if parent:
            os.makedirs(parent, exist_ok=True)

    conn = sqlite3.connect(path, check_same_thread=False)
    registry = GraphArtifactRegistry(conn)
    try:
        yield registry
    finally:
        registry.close()
