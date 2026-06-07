from app.schemas import EngineeringGraph


def is_point_in_polygon(point: list[float], polygon: list[list[float]]) -> bool:
    """Ray-casting algorithm to determine if a point is inside a polygon.

    Args:
        point: [x, y] coordinates.
        polygon: List of [x, y] coordinates forming a closed or unclosed polygon.

    Returns:
        True if point is inside, False otherwise.
    """
    if not point or not polygon or len(polygon) < 3:
        return False

    x, y = point[0], point[1]
    is_inside = False

    n = len(polygon)
    j = n - 1

    for i in range(n):
        xi, yi = polygon[i][0], polygon[i][1]
        xj, yj = polygon[j][0], polygon[j][1]

        intersect = ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi)
        if intersect:
            is_inside = not is_inside

        j = i

    return is_inside


def fuse_graphs(
    architecture: EngineeringGraph, mep: EngineeringGraph
) -> tuple[EngineeringGraph, list[str]]:
    """Fuse architectural and MEP graphs, assigning MEP nodes to architectural spaces.

    Args:
        architecture: The base architectural EngineeringGraph containing spaces.
        mep: The MEP EngineeringGraph containing nodes to be assigned.

    Returns:
        A tuple of (fused EngineeringGraph, list of warning strings).
    """
    warnings: list[str] = []

    # Create the fused graph starting with architecture
    fused_meta = architecture.meta.model_copy()
    if mep.meta.title:
        if fused_meta.title:
            fused_meta.title = f"{fused_meta.title} + {mep.meta.title}"
        else:
            fused_meta.title = mep.meta.title

    if not fused_meta.diagram_type and mep.meta.diagram_type:
        fused_meta.diagram_type = "fused"
    elif fused_meta.diagram_type:
        fused_meta.diagram_type = "fused"

    fused = EngineeringGraph(
        meta=fused_meta,
        spaces=architecture.spaces.copy() + mep.spaces.copy(),
        walls=architecture.walls.copy() + mep.walls.copy(),
        fixtures=architecture.fixtures.copy() + mep.fixtures.copy(),
        nodes=architecture.nodes.copy(),
        edges=architecture.edges.copy() + mep.edges.copy(),
        annotations=architecture.annotations.copy() + mep.annotations.copy(),
    )

    # Process MEP nodes and try to assign them to spaces
    for node in mep.nodes:
        new_node = node.model_copy()
        if new_node.position:
            assigned = False
            for space in fused.spaces:
                if space.polygon and is_point_in_polygon(new_node.position, space.polygon):
                    new_node.space_id = space.space_id
                    assigned = True
                    break

            if not assigned:
                warnings.append(
                    f"Node {new_node.node_id} at position {new_node.position} "
                    "could not be assigned to any space."
                )
        else:
            warnings.append(
                f"Node {new_node.node_id} has no position and could not be assigned to any space."
            )

        fused.nodes.append(new_node)

    return fused, warnings
