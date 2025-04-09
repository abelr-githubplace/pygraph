from collections import deque
import graph

## ITER
def build_subgraph(self, src: int, distance: int) -> graph.Graph:
    """Build the undirected subgraph of the graph G with nodes at a threshold distance from src.
    """

    subG = graph.Graph(1, False)
    queue= deque()

    # Set all nodes to no distance from src
    dist= [-1] * self.order

    # Keep track of node number from G to subG
    index_map = [None] * self.order

    # Visit src
    dist[src] = 0
    index_map[src] = 0
    queue.append(src)

    while not queue:
        node = queue.popleft()
        for neigh in self.adjlists[node]:
            # Not visited and in reach
            if dist[neigh] == -1 and dist[node] < distance:
                # Update distance
                dist[neigh] = dist[node] + 1

                subG.add_node()

                # Keep track of node number
                index_map[neigh] = subG.order - 1

                queue.append(neigh)

                # Add neighbour to subgraph adjacency list of node
                subG.adjlists[index_map[node]].append(index_map[neigh])

    return subG