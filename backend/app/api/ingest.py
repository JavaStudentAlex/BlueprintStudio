"""Document ingestion endpoint.

Accepts one or more uploaded files (PDF / Markdown / plain text), saves them
to the gitignored documents directory, and pushes their chunks into the KB.

The same code path is also used by `services.ingestion.ingest_directory()` to
slurp up files dropped into `backend/data/documents/` at startup.
"""

from __future__ import annotations

import hashlib
import io
import json
import os
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, File, Form, HTTPException, Request, Response, UploadFile
from PIL import Image, ImageDraw
from pydantic import ValidationError

from app.schemas import EngineeringGraph, IngestResponse
from app.services.engineering_converters import get_engineering_converter
from app.services.engineering_files import classify
from app.services.ingestion import (
    RegisteredIngestFile,
    classify_and_route_registered_files,
    ingest_registered_files,
)

router = APIRouter(prefix="/api", tags=["ingest"])


@dataclass(frozen=True, slots=True)
class _PreparedUpload:
    original_filename: str
    extension: str
    content_type: str
    body: bytes
    content_hash: str
    byte_size: int


@router.post("/ingest", response_model=IngestResponse)
async def ingest(
    request: Request,
    files: Annotated[list[UploadFile], File(...)],
) -> IngestResponse:
    if not files:
        raise HTTPException(status_code=400, detail="no files provided")

    state = request.app.state.app_state
    documents_dir = state.settings.documents_dir
    os.makedirs(documents_dir, exist_ok=True)

    prepared_uploads = await _prepare_uploads(
        files,
        max_upload_bytes=state.settings.max_upload_bytes,
    )
    entries: list[RegisteredIngestFile] = []
    processing_document_ids: set[str] = set()

    for upload in prepared_uploads:
        document_id = uuid.uuid4().hex
        stored_path = os.path.join(documents_dir, f"{document_id}{upload.extension}")
        record, is_duplicate = state.registry.register_or_get(
            upload.content_hash,
            original_filename=upload.original_filename,
            stored_path=stored_path,
            content_type=upload.content_type,
            byte_size=upload.byte_size,
            document_id=document_id,
        )
        should_process = not is_duplicate
        if (
            is_duplicate
            and record.status == "uploaded"
            and record.document_id not in processing_document_ids
        ):
            should_process = True
        if should_process:
            processing_document_ids.add(record.document_id)
        if should_process and (not is_duplicate or not os.path.exists(record.stored_path)):
            with open(record.stored_path, "wb") as out:
                out.write(upload.body)
        entries.append(
            RegisteredIngestFile(
                record=record,
                is_duplicate=not should_process,
                classification=classify(upload.original_filename),
            )
        )

    engineering_converter = state.engineering_converter or get_engineering_converter(state.settings)
    routed_entries = classify_and_route_registered_files(state.registry, entries)
    return await ingest_registered_files(
        state.kb,
        state.registry,
        routed_entries,
        document_analyzer=state.document_analyzer,
        engineering_converter=engineering_converter,
        engineering_converter_output_dir=state.engineering_converter_output_dir,
        graph_artifacts=state.graph_artifacts,
        drawing_parser=state.drawing_parser,
    )


async def _prepare_uploads(
    files: list[UploadFile],
    *,
    max_upload_bytes: int,
) -> list[_PreparedUpload]:
    prepared: list[_PreparedUpload] = []
    for upload in files:
        filename = _validated_filename(upload.filename)
        extension = os.path.splitext(filename)[1].lower()
        body = await upload.read(max_upload_bytes + 1)
        if len(body) > max_upload_bytes:
            raise HTTPException(status_code=413, detail="uploaded file is too large")
        if not body:
            raise HTTPException(status_code=400, detail="uploaded file is empty")
        prepared.append(
            _PreparedUpload(
                original_filename=filename,
                extension=extension,
                content_type=upload.content_type or "",
                body=body,
                content_hash=hashlib.sha256(body).hexdigest(),
                byte_size=len(body),
            )
        )

    if not prepared:
        raise HTTPException(status_code=400, detail="no valid files in upload")
    return prepared


def _validated_filename(filename: str | None) -> str:
    clean_name = (filename or "").strip()
    basename = os.path.basename(clean_name)
    if not basename:
        raise HTTPException(status_code=400, detail="uploaded file is missing a filename")
    return basename


@router.get("/demo/floorplan")
async def demo_floorplan():
    fixture_path = Path("tests/fixtures/flowdraft/demo_floorplan.json")
    with open(fixture_path) as f:
        return json.load(f)


@router.get("/demo/compliance-graph")
async def demo_compliance_graph():
    fixture_path = Path("tests/fixtures/flowdraft/demo_datacentre.json")
    with open(fixture_path) as f:
        return json.load(f)


@router.get("/demo/compliance-report")
async def demo_compliance_report():
    fixture_path = Path("tests/fixtures/flowdraft/demo_compliance_report.json")
    with open(fixture_path) as f:
        return json.load(f)


@router.post("/overlay")
async def overlay(image: Annotated[UploadFile, File(...)], graph: Annotated[str, Form(...)]):
    try:
        graph_data = json.loads(graph)
        eng_graph = EngineeringGraph.model_validate(graph_data)
    except (json.JSONDecodeError, ValidationError) as e:
        raise HTTPException(status_code=400, detail="Invalid graph payload") from e

    image_bytes = await image.read()
    try:
        pil_img = Image.open(io.BytesIO(image_bytes))
        pil_img.load()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image payload") from e

    draw = ImageDraw.Draw(pil_img)

    # Draw spaces as polygons
    for space in eng_graph.spaces:
        if space.polygon:
            coords = [(p[0], p[1]) for p in space.polygon]
            if len(coords) >= 2:
                draw.polygon(coords, outline="blue", width=3)

    # Draw nodes as circles
    for node in eng_graph.nodes:
        if node.position:
            x, y = node.position[0], node.position[1]
            draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill="red", outline="red")

    # Draw edges as lines
    for edge in eng_graph.edges:
        if edge.polyline:
            coords = [(p[0], p[1]) for p in edge.polyline]
            if len(coords) >= 2:
                draw.line(coords, fill="green", width=3)

    out_bytes = io.BytesIO()

    if pil_img.mode != "RGB":
        pil_img = pil_img.convert("RGB")  # type: ignore[assignment]

    pil_img.save(out_bytes, format="JPEG")
    return Response(content=out_bytes.getvalue(), media_type="image/jpeg")
