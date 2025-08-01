## EXP4: Distance Vector Routing Protocol Simulation

This experiment implements and simulates the Distance Vector Routing Protocol in Python, including Split Horizon with Poison Reverse to prevent routing loops.

---

### Overview

Each router discovers shortest paths to all destinations by exchanging distance vectors with its neighbors. The protocol iteratively updates routing tables until convergence.

---

### Steps

#### 1. Initialization

- For each router, initialize its distance vector:
  - Cost to self = 0, next hop = self.
  - Cost to each immediate neighbor = link cost, next hop = that neighbor.
- Enable Split Horizon with Poison Reverse if mitigating count-to-infinity.

#### 2. Iterative Update (Synchronous Rounds)

1. **For each router:** prepare an update for every neighbor:
   - For each destination in its vector:
     - If using poison reverse and the route’s next hop is that neighbor, advertise cost = ∞ for that destination.
     - Otherwise, advertise the current cost.
2. **Exchange:** deliver each prepared vector to the corresponding neighbor.
3. **For each receiving router:** for each incoming vector from a neighbor:
   - For each destination in the incoming vector:
     - Compute potential cost = cost to that neighbor + advertised cost.
     - If potential cost is lower than current, update distance and set next hop = that neighbor.
     - If current route uses that neighbor and the neighbor now advertises ∞, invalidate that route.
4. After all updates in the round, check if any router’s table changed:
   - If yes, repeat the update round.
   - If no, convergence achieved; stop.

#### 3. Optional Maintenance

- Expire or garbage-collect stale routes to bound memory.

---