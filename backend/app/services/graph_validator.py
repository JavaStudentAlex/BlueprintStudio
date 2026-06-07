from typing import Any

from pydantic import ValidationError

from app.schemas import EngineeringGraph, GraphValidationError


def validate_graph(data: dict[str, Any] | EngineeringGraph) -> list[GraphValidationError]:
    """Validate a graph payload structurally and semantically."""
    errors: list[GraphValidationError] = []

    # 1. Structural validation via Pydantic
    graph_obj = None
    if isinstance(data, EngineeringGraph):
        graph_obj = data
    else:
        try:
            graph_obj = EngineeringGraph.model_validate(data)
        except ValidationError as e:
            for err in e.errors():
                path = ".".join(str(p) for p in err["loc"])
                msg = err["msg"]
                code = "validation_error"
                if err["type"] == "extra_forbidden":
                    code = "unsupported_field"
                elif err["type"] == "literal_error":
                    code = "invalid_value"

                errors.append(
                    GraphValidationError(
                        path=path,
                        code=code,
                        message=msg,
                        severity="error",
                    )
                )

    if not graph_obj:
        return errors

    # 2. Semantic validation: Ensure edge sources and targets exist
    # Collect all valid entity IDs
    entity_ids = set()
    for space in graph_obj.spaces:
        entity_ids.add(space.space_id)
    for wall in graph_obj.walls:
        entity_ids.add(wall.wall_id)
    for fixture in graph_obj.fixtures:
        entity_ids.add(fixture.fixture_id)
    for node in graph_obj.nodes:
        entity_ids.add(node.node_id)
    for annotation in graph_obj.annotations:
        entity_ids.add(annotation.annotation_id)

    for i, edge in enumerate(graph_obj.edges):
        if edge.source_id not in entity_ids:
            errors.append(
                GraphValidationError(
                    path=f"edges.{i}.source_id",
                    code="missing_node",
                    message=f"Edge references non-existent source_id: {edge.source_id}",
                    severity="error",
                )
            )
        if edge.target_id not in entity_ids:
            errors.append(
                GraphValidationError(
                    path=f"edges.{i}.target_id",
                    code="missing_node",
                    message=f"Edge references non-existent target_id: {edge.target_id}",
                    severity="error",
                )
            )

    return errors
