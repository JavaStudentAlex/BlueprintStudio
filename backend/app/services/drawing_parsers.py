"""Parser adapter contract for converting uploaded drawings to graphs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Protocol

from app.schemas import EngineeringGraph, GraphProvenance

DrawingRouting = Literal["FLOORPLAN", "PID", "SLD", "AUTO"]


@dataclass(frozen=True, slots=True)
class ParserResult:
    """The result of parsing a drawing file into an engineering graph."""

    graph: EngineeringGraph
    warnings: list[str] = field(default_factory=list)
    confidence: float | None = None
    parser_name: str | None = None
    provenance: GraphProvenance | None = None


class DrawingParserAdapter(Protocol):
    """Protocol for parser engines that emit graph artifacts from files."""

    def parse_drawing(self, file_path: str, *, routing: DrawingRouting = "AUTO") -> ParserResult:
        """Parse the given drawing file using the requested routing mode."""
