# Metro / Subway Route Optimizer Documentation

## 1. Problem Formulation & PEAS

### PEAS Description
*   **Performance Measure**: 
    *   Minimum travel time between two stations.
    *   Minimum number of transfers (line changes).
    *   Total number of stations visited (efficiency).
*   **Environment**: 
    *   A static graph representation of a city's metro network.
    *   Nodes represent stations, and edges represent the rail lines connecting them.
    *   Weights on edges represent travel time in minutes.
*   **Actuators**: 
    *   The pathfinding agent outputs the optimal sequence of stations and lines to take.
    *   Instructions on where to transfer lines.
*   **Sensors**: 
    *   Input of the current starting station.
    *   Input of the desired destination station.
    *   Internal database of the metro graph and line information.

### State Space
*   **Structure**: A complex Graph $G = (V, E)$ containing multiple cycles (loops).
*   **Nodes ($V$)**: Individual metro stations.
*   **Edges ($E$)**: Connections including three main lines (Blue, Red, Green) and an outer "Yellow" loop.
*   **Weights**: Variable travel times on each edge.
*   **Advanced Feature**: Transfer cost $C = 5$ mins added when switching between lines.

### States & Actions
*   **Initial State**: The station where the passenger is currently located.
*   **Goal State**: The destination station the passenger wants to reach.
*   **Valid Actions**: Moving from the current station to any adjacent station connected by a rail line.

---

## 2. Search Algorithms Implementation

The following algorithms are implemented to find the path:

1.  **Breadth-First Search (BFS)**:
    *   Explores neighbor nodes first before moving to the next level.
    *   **Optimality**: Guarantees the path with the fewest stations (edges), but not necessarily the shortest time if weights vary.
    *   **Data Structure**: Queue (FIFO).

2.  **Depth-First Search (DFS)**:
    *   Explores as far as possible along each branch before backtracking.
    *   **Optimality**: Does not guarantee the shortest path.
    *   **Data Structure**: Stack (LIFO).

3.  **Dijkstra's Algorithm**:
    *   Finds the path with the minimum total weight (time).
    *   **Optimality**: Guarantees the optimal path based on weights and transfer costs.
    *   **Data Structure**: Priority Queue.

---

## 4. Graphical User Interface (GUI)

The project includes a premium desktop GUI built with **Python** using the following libraries:
- **CustomTkinter**: For a modern, high-fidelity dark theme.
- **Tkinter Canvas**: For custom graph rendering and animations.

### GUI Features:
1.  **Interactive Map**: A visual representation of the metro network with color-coded lines.
2.  **Algorithm Selection**: Toggle between BFS, DFS, and Dijkstra.
3.  **Real-time Animation**: The path lights up step-by-step as the algorithm finds the route.
4.  **Live Metrics**: Displays the number of expanded nodes, path length, and total travel time immediately after execution.
