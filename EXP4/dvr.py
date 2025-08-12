import copy

class DistanceVectorRouting:
    def __init__(self, graph):
        """
        graph: dict of dict where graph[u][v] = cost from u to v (inf if no direct link)
        """
        self.graph = graph
        self.nodes = list(graph.keys())
        self.dist_vectors = {node: {n: float('inf') for n in self.nodes} for node in self.nodes}
        self.next_hops = {node: {n: None for n in self.nodes} for node in self.nodes}
        # Distance to self is 0
        for node in self.nodes:
            self.dist_vectors[node][node] = 0
            for neighbor in self.graph[node]:
                if self.graph[node][neighbor] != float('inf'):
                    self.dist_vectors[node][neighbor] = self.graph[node][neighbor]
                    self.next_hops[node][neighbor] = neighbor

    def run(self, max_iterations=100):
        """
        Run the Distance Vector Routing algorithm until convergence or max_iterations.
        Print each step of the algorithm.
        """
        print("\nInitial State:")
        self.print_dist_vectors()

        for iteration in range(max_iterations):
            print(f"\nIteration {iteration + 1}:")
            updated = False
            old_dist_vectors = copy.deepcopy(self.dist_vectors)

            for node in self.nodes:
                for neighbor in self.graph[node]:
                    if self.graph[node][neighbor] == float('inf'):
                        continue
                    for dest in self.nodes:
                        if old_dist_vectors[neighbor][dest] == float('inf'):
                            continue
                        new_cost = self.graph[node][neighbor] + old_dist_vectors[neighbor][dest]
                        if new_cost < self.dist_vectors[node][dest]:
                            self.dist_vectors[node][dest] = new_cost
                            self.next_hops[node][dest] = neighbor
                            updated = True

            self.print_dist_vectors()

            if not updated:
                print("Converged!")
                break

    def print_dist_vectors(self):
        print("\nRouting Tables:")
        for node in self.nodes:
            print(f"\nNode {node}:")
            print("Destination | Cost | Next Hop")
            print("-----------------------------")
            for dest in self.nodes:
                cost = self.dist_vectors[node][dest]
                cost_str = "inf" if cost == float('inf') else str(cost)
                next_hop = self.next_hops[node][dest] or "-"
                print(f"{dest:<11} | {cost_str:<4} | {next_hop}")

def get_user_input_graph():
    num_nodes = int(input("Enter the number of nodes: "))
    node_names = input(f"Enter the names of the {num_nodes} nodes (space-separated): ").split()

    graph = {node: {} for node in node_names}
    for node in node_names:
        for other in node_names:
            if node == other:
                graph[node][other] = 0
            else:
                graph[node][other] = float('inf')

    print("\nEnter cost between each unique pair of nodes (undirected, enter 'inf' if no direct link):")
    for i in range(num_nodes):
        for j in range(i+1, num_nodes):
            src = node_names[i]
            dest = node_names[j]
            cost_input = input(f"Cost between {src} and {dest}: ").strip()
            cost = float('inf') if cost_input.lower() == 'inf' else float(cost_input)
            graph[src][dest] = cost
            graph[dest][src] = cost

    return graph

if __name__ == "__main__":
    user_graph = get_user_input_graph()
    dvr = DistanceVectorRouting(user_graph)
    dvr.run()
