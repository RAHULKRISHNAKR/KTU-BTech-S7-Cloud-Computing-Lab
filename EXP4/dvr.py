import copy

INFINITY = 1_000_000

class Router:
    def __init__(self, name, neighbors, split_horizon_poison=False):
        """
        neighbors: dict of neighbor_name -> cost
        """
        self.name = name
        self.neighbors = neighbors  # direct link costs
        self.split_horizon_poison = split_horizon_poison

        # distance vector: destination -> (cost, next_hop)
        self.dv = {self.name: (0, self.name)}
        for nbr, cost in neighbors.items():
            self.dv[nbr] = (cost, nbr)

    def prepare_update_for(self, neighbor_name):
        """
        Prepare the vector to send to a neighbor, applying split horizon with poison reverse if enabled.
        Returns a dict: destination -> cost advertised.
        """
        update = {}
        for dest, (cost, next_hop) in self.dv.items():
            advertised_cost = cost
            if self.split_horizon_poison and next_hop == neighbor_name and dest != neighbor_name:
                # poison reverse: tell neighbor the route through it is infinite
                advertised_cost = INFINITY
            update[dest] = advertised_cost
        return update

    def process_incoming(self, from_router, incoming_vector):
        """
        Bellman-Ford update using incoming vector from a neighbor.
        incoming_vector: dict dest -> advertised cost (already processed with split horizon logic by sender)
        Returns True if any change occurred.
        """
        changed = False
        cost_to_neighbor = self.neighbors.get(from_router, INFINITY)
        for dest, adv_cost in incoming_vector.items():
            if dest == self.name:
                continue  # skip self

            new_cost = adv_cost + cost_to_neighbor
            current_cost, current_next = self.dv.get(dest, (INFINITY, None))
            if new_cost < current_cost:
                self.dv[dest] = (new_cost, from_router)
                changed = True
            else:
                # if current route uses that neighbor and its advertised cost increased, update (triggered by poisoned info)
                if current_next == from_router and adv_cost == INFINITY and current_cost != INFINITY:
                    # invalidate route via that neighbor
                    self.dv[dest] = (INFINITY, None)
                    changed = True
        return changed

    def routing_table(self):
        """
        Returns a copy of current routing table in readable form.
        """
        table = {}
        for dest, (cost, next_hop) in self.dv.items():
            table[dest] = (cost if cost < INFINITY else None, next_hop)
        return table

    def __str__(self):
        lines = [f"Router {self.name} routing table:"]
        for dest, (cost, next_hop) in sorted(self.routing_table().items()):
            cost_str = str(cost) if cost is not None else "∞"
            nh = next_hop if next_hop is not None else "-"
            lines.append(f"  to {dest:>3}: cost={cost_str:>4}, next_hop={nh}")
        return "\n".join(lines)


def simulate(routers: dict, max_rounds=100):
    """
    routers: name -> Router instance
    Runs synchronous rounds: each router exchanges its vector with neighbors.
    Stops when no updates occur in a full round or max_rounds reached.
    """
    print("=== Starting Distance Vector Simulation ===")
    for r in routers.values():
        print(r)
    print("------------------------------------------")

    for round_num in range(1, max_rounds + 1):
        print(f"\n--- Round {round_num} ---")
        updates = {}  # router_name -> list of (from_neighbor, vector)
        # Each router prepares what it would send to each neighbor
        for name, router in routers.items():
            for nbr in router.neighbors:
                if nbr not in routers:
                    continue  # skip if neighbor missing
                vec = router.prepare_update_for(nbr)
                updates.setdefault(nbr, []).append( (name, vec) )

        any_change = False
        # Deliver updates
        for receiver_name, incoming_list in updates.items():
            receiver = routers[receiver_name]
            for sender_name, vector in incoming_list:
                changed = receiver.process_incoming(sender_name, vector)
                if changed:
                    any_change = True

        for r in routers.values():
            print(r)
        if not any_change:
            print(f"\nConverged in {round_num} rounds.")
            break
    else:
        print("\nReached max rounds without full convergence.")

# Example usage / demonstration
if __name__ == "__main__":
    # Define topology: adjacency with costs
    # A --1-- B
    # |       |
    # 4       2
    # |       |
    # C --1-- D
    #
    # Plus extra link A--5--D to create multiple paths.

    topo = {
        'A': {'B': 1, 'C': 4, 'D': 5},
        'B': {'A': 1, 'D': 2},
        'C': {'A': 4, 'D': 1},
        'D': {'B': 2, 'C': 1, 'A': 5},
    }

    # Instantiate routers with split horizon with poison reverse enabled
    routers = {name: Router(name, neighbors, split_horizon_poison=True) for name, neighbors in topo.items()}

    simulate(routers)
