## EXP4: Distance Vector Routing Protocol Simulation

This experiment implements a synchronous simulation of the Distance Vector Routing (Bellman–Ford style) algorithm in Python. The current script (`dvr.py`) runs an iterative convergence process over a user‑defined undirected weighted graph.

---
### Features Implemented
- User prompts to build an undirected graph (node names + pairwise link costs or `inf`).
- Internal initialization of distance vectors and next hops.
- Iterative relaxation across all node pairs through neighbors until no improvement.
- Per‑iteration printing of every node's routing table (destination, cost, next hop).
- Early stop on convergence (no updates in an iteration) or after `max_iterations` (default 100).

---
### Not Implemented (Yet)
- Split Horizon / Poison Reverse.
- Route invalidation on link failure.
- Asynchronous update ordering (currently synchronous global rounds via deep copy snapshot).
- Negative edge weight handling (assumes non‑negative costs or `inf`).
- Detection of count‑to‑infinity scenarios.

---
### File
- `dvr.py`: Contains `DistanceVectorRouting` class and an interactive `get_user_input_graph()` builder.

---
### Algorithm Outline
For each iteration (round):
1. Snapshot current distance vectors (deep copy).
2. For every node `u` and each directly connected neighbor `v` (finite link cost):
   - For each destination `d` with a finite cost in neighbor's snapshot: compute `cost(u,v) + dist_v[d]`.
   - If this new cost is lower than current `dist_u[d]`, update `dist_u[d]` and set next hop to `v`.
3. After processing all nodes, print updated routing tables.
4. If no updates occurred, declare convergence.

---
### Data Structures
- `self.graph`: adjacency dict `graph[u][v] = cost` (symmetric for undirected input).
- `self.dist_vectors[u][d]`: current best known cost from `u` to destination `d`.
- `self.next_hops[u][d]`: next hop neighbor chosen from `u` toward `d`.

---
### Running the Simulation
```
python dvr.py
```
Input example:
```
Enter the number of nodes: 3
Enter the names of the 3 nodes (space-separated): A B C
Enter cost between each unique pair of nodes (undirected, enter 'inf' if no direct link):
Cost between A and B: 4
Cost between A and C: 2
Cost between B and C: 5
```
Sample output excerpt:
```
Initial State:
Routing Tables:
Node A:
Destination | Cost | Next Hop
...
Iteration 1:
...
Converged!
```

---
### Example Interpretation
If `A` connects to `B` (4) and `C` (2), and `B`–`C` is 5, then after convergence:
- `A` → `B` shortest cost may remain 4 (direct) unless an alternate cheaper path emerges.
- `B` → `A` may stay 4; `B` → `C` will be min(5 direct, 4+2 via A,  ... ).
- `A` → `C` is 2 (direct).

---
### Extending the Implementation
Potential enhancements:
1. Add Split Horizon with Poison Reverse when advertising vectors.
2. Simulate link failures and trigger recalculation.
3. Convert synchronous rounds into event-driven asynchronous neighbor updates.
4. Add max cost threshold (simulate RIP's infinity = 16) and count‑to‑infinity detection.
5. Export routing evolution to a CSV or JSON timeline.
6. Add a visualization layer (e.g., `networkx` + `matplotlib`).

---
### Code Entry Points
- Class: `DistanceVectorRouting(graph)`
- Method: `run(max_iterations=100)` performs convergence.
- Helper: `get_user_input_graph()` builds adjacency dict from user input.

---
### Quick API Usage (Programmatic)
```python
from dvr import DistanceVectorRouting

graph = {
  'A': {'A': 0, 'B': 4, 'C': 2},
  'B': {'A': 4, 'B': 0, 'C': 5},
  'C': {'A': 2, 'B': 5, 'C': 0},
}
router = DistanceVectorRouting(graph)
router.run()
```

---
### Notes
Ensure all non‑existent links are represented with `float('inf')` for correctness. The current input helper enforces symmetric costs.

---