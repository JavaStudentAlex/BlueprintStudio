"""Tests for drawing parser adapter contracts."""

from __future__ import annotations

import pytest

from app.schemas import EngineeringGraph, GraphMeta, GraphProvenance
from app.services.drawing_parsers import (
    DrawingParserAdapter,
    DrawingRouting,
    ParserResult,
)


class FakeDrawingParserAdapter:
    """A fake parser engine adapter for testing."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, DrawingRouting]] = []

    def parse_drawing(self, file_path: str, *, routing: DrawingRouting = "AUTO") -> ParserResult:
        self.calls.append((file_path, routing))

        # Determine diagram type roughly based on routing mode
        diagram_type = "fused"
        if routing == "FLOORPLAN":
            diagram_type = "floorplan"
        elif routing == "PID":
            diagram_type = "pid"
        elif routing == "SLD":
            diagram_type = "sld"

        graph = EngineeringGraph(
            meta=GraphMeta(
                diagram_type=diagram_type,
                title=f"Fake parsed {routing}",
            )
        )

        return ParserResult(
            graph=graph,
            warnings=["Fake warning for testing"],
            confidence=0.95,
            parser_name="fake-drawing-parser",
            provenance=GraphProvenance(
                source_file=file_path,
                parser_engine="fake-drawing-parser",
                confidence=0.95,
            ),
        )


def test_fake_drawing_parser_conforms_to_protocol() -> None:
    # This will fail type checking if FakeDrawingParserAdapter doesn't match
    # the DrawingParserAdapter protocol.
    adapter: DrawingParserAdapter = FakeDrawingParserAdapter()

    result = adapter.parse_drawing("test_file.pdf")
    assert result.parser_name == "fake-drawing-parser"
    assert result.confidence == 0.95
    assert result.warnings == ["Fake warning for testing"]
    assert result.provenance is not None
    assert result.provenance.source_file == "test_file.pdf"


@pytest.mark.parametrize(
    "routing, expected_diagram_type",
    [
        ("FLOORPLAN", "floorplan"),
        ("PID", "pid"),
        ("SLD", "sld"),
        ("AUTO", "fused"),
    ],
)
def test_fake_drawing_parser_handles_routing(
    routing: DrawingRouting, expected_diagram_type: str
) -> None:
    adapter = FakeDrawingParserAdapter()
    result = adapter.parse_drawing("test_file.pdf", routing=routing)

    assert result.graph.meta.diagram_type == expected_diagram_type
    assert result.graph.meta.title == f"Fake parsed {routing}"
    assert adapter.calls == [("test_file.pdf", routing)]
