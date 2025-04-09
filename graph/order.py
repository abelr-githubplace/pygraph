## ITER
def topological_order(self) -> list[int]:
    """Topological order of nodes in graph G.
    """

    node_degrees = [0] * self.order
    nodes = []

    # Get node degrees
    for node in range(self.order):
        for neigh in self.adjlists[node]:
            node_degrees[neigh] += 1

    # Insert nodes of degree 0
    capacity = 0
    for node in range(self.order):
        if node_degrees[node] == 0:
            nodes.append(node)
            capacity += 1

    # Insert other nodes when visited degree-th times by expanding from already inserted nodes
    index = 0
    while capacity < self.order:
        if index == capacity:
            raise Exception("Graph is cyclic")
        for neigh in self.adjlists[nodes[index]]:
            node_degrees[neigh] -= 1
            if node_degrees[neigh] == 0:
                nodes.append(neigh)
                capacity += 1
        index += 1
    
    return nodes