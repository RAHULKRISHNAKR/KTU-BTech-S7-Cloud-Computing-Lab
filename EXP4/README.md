### using python implement and simulate an algorithm for distance vector routing protocol

### Distance Vector Routing Protocol (with Split Horizon + Poison Reverse)

**Goal:** Each router discovers shortest paths to all destinations via neighbor exchanges.

#### Initialization

1. For each router, initialize its distance vector:

   * Cost to self = 0, next hop = self.
   * Cost to each immediate neighbor = link cost, next hop = that neighbor.
2. Enable `split horizon with poison reverse` flag if mitigating count-to-infinity.

#### Iterative update (synchronous rounds)

3. **For each router:** prepare an update for every neighbor:

   * For each destination in its vector:

     * If using poison reverse and the route’s next hop is that neighbor, advertise cost = ∞ for that destination.
     * Otherwise advertise the current cost.

4. **Exchange:** deliver each prepared vector to the corresponding neighbor.

5. **For each receiving router:** for each incoming vector from a neighbor:

   * For each destination in the incoming vector:

     * Compute potential cost = cost to that neighbor + advertised cost.
     * If potential cost is lower than current, update distance and set next hop = that neighbor.
     * If current route uses that neighbor and the neighbor now advertises ∞, invalidate that route.

6. After all updates in the round, check if **any** router’s table changed.

   * If yes, repeat step 3 (next round).
   * If no, **convergence** achieved; stop.

#### Optional maintenance

7. (Optional) Expire or garbage-collect stale routes to bound memory.

---