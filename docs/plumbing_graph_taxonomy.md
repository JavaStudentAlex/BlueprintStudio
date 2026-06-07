# Plumbing Graph Taxonomy

## Overview

This document defines the vocabulary and concepts used to represent plumbing networks within the BlueprintStudio canonical engineering graph. The plumbing taxonomy aligns with the general graph structures defined in the backend schemas (`GraphFixture`, `GraphNode`, `GraphEdge`) to support modeling water supply, drainage, and waste systems.

## Vocabulary

### 1. Plumbing Nodes (`GraphNode`)
These represent internal connection points, junctions, or inline components within a plumbing network.

*   **Valves:** Flow control devices (e.g., isolation valves, check valves, pressure reducing valves).
*   **Drains:** Collection points for waste or storm water (e.g., floor drains, roof drains).
*   **Risers:** Vertical pipe sections that distribute water between floors.
*   **Fittings:** Junctions such as tees, elbows, or crosses where pipe direction or diameter changes.

### 2. Plumbing Fixtures (`GraphFixture`)
These represent endpoint equipment items that consume or discharge water.

*   **Plumbing Fixtures:** Sinks, toilets, showers, bathtubs, and urinals.
*   **Meters:** Devices that measure water usage or flow.
*   **Pumps:** Devices that move or pressurize water (e.g., booster pumps, sump pumps, circulation pumps).
*   **Tanks:** Storage vessels for water (e.g., hot water heaters, expansion tanks).

### 3. Plumbing Edges (`GraphEdge`)
These represent the physical connections and flow paths between nodes and fixtures.

*   **Pipes:** The physical conduits connecting components.
*   **Water Supply Systems:** Edges representing domestic cold water (DCW), domestic hot water (DHW), or industrial water lines.
*   **Drainage/Waste Systems:** Edges representing sanitary waste, storm drainage, or condensate lines.

## Future Validation Examples

When performing compliance or topological checks on the plumbing graph, the following examples illustrate potential validations:

1.  **Flow Direction:** Validating that water flows correctly from source (e.g., meter or pump) to endpoints (fixtures), and that waste flows from fixtures to drains without cyclical paths.
2.  **Pipe Sizing:** Checking that upstream pipes have sufficient diameter to handle the accumulated downstream fixture unit demand.
3.  **Valve Placement:** Ensuring that critical equipment (like pumps or water heaters) or major branches have the required isolation valves.
4.  **Connectivity Checks:** Verifying that a fixture requiring hot water is actually connected to a hot water supply network, and that its waste outlet is connected to the sanitary drainage system.
