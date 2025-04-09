## ITER
def is_colored_nicely(self, color: list[int]) -> bool:
    """Check if graph G is colored correctly.
    """

    # Get the set of the neighboors of each node
    neighbours = [set()] * self.order
    for node in range(self.order):
        for neigh in self.adjlists[node]:
            neighbours[neigh].add(node)
            neighbours[node].add(neigh)
        
    # Check a color is not next to itself
    for node in range(self.order):
        for neigh in neighbours[node]:
            if color[neigh] == color[node]:
                return False
    
    return True