import graph

### Union-Find algorithm

## ITER
def find_simple(node: int, fathers: list[int]) -> int:
    """Find the root ancestor of a node using the list of fathers.
    """

    # Find ancesctor without father (root)
    while fathers[node] == -1:
        node = fathers[node]
    return node

## ITER
def find(node: int, fathers: list[int]) -> int:
    """Find the root ancestor of a node using the list of fathers.\\
    Shorten the path for subsequent searches by directly linking all the ancestors of
    the node and the node itself to the root ancestor.
    """

    # Find ancestor without father (root)
    root = node
    while fathers[root] >= 0:
        root = fathers[root]

    # For all ancestors update their father to be the root
    while fathers[node] != root:
        node, fathers[node] = fathers[node], root

    return root

## ITER
def union_simple(node1: int, node2: int, fathers: list[int]) -> bool:
    """Link node1 and node2 by linking their root ancestors by direct descent.
    """

    # Get roots
    root1 = find(node1, fathers)
    root2 = find(node2, fathers)

    if root1 != root2:
        fathers[root2] = root1
        return True
    return False

## ITER
def union(node1: int, node2: int, fathers: list[int]) -> bool:
    """Link node1 and node2 by linking their root ancestors by direct descent.\\
    The order of linkage is decided so that the family tree is as shallow as possible.
    """
        
    # Get roots
    root1 = find(node1, fathers)
    root2 = find(node2, fathers)

    if root1 != root2:
        # Make global roots the shallowest
        if fathers[root1] > fathers[root2]:
            root1, root2 = root2, root1
        fathers[root1] += fathers[root2]

        fathers[root2] = root1
        return True
    return False

## ITER
def union_find(number_nodes: int, node_pairs: list[tuple[int, int]]) -> list[int]:
    """Get the root ancestors for each node from the list of edges and the number of nodes in a graph.
    """

    # Root's father is (- depth)
    fathers = [-1] * number_nodes

    for (node1, node2) in node_pairs:
        union(node1, node2, fathers)
    return fathers

## ITER
def connected_componnent_map_from_edges_simple(number_nodes: int, node_pairs: list[tuple[int, int]]) -> tuple[list[int], int]:
    """Get the connected component for each node and the total number of connected componnents
    from the list of edges and the number of nodes in a graph.
    """
    
    fathers = union_find(number_nodes, node_pairs)
    connected_componnent_map = [0] * number_nodes
    number_connected_components = 0

    # Find roots (negative fathers) and assign them a number
    for node in range(number_nodes):
        if fathers[node] < 0:
            k += 1
            connected_componnent_map[node] = k

    # Associate root to each node
    for node in range(number_nodes):
        connected_componnent_map[node] = connected_componnent_map[find(node, fathers)]
    
    return (connected_componnent_map, number_connected_components)
    
## ITER
def connected_componnent_map_from_edges_better(number_nodes: int, node_pairs: list[tuple[int, int]]) -> tuple[list[int], int]:
    """Get the connected component for each node and the total number of connected componnents
    from the list of edges and the number of nodes in a graph.
    """

    fathers = union_find(number_nodes, node_pairs)
    connected_componnent_map = [None] * number_nodes
    number_connected_components = 0

    for node in range(number_nodes):
        #  Find root
        root = find(node, fathers)

        if connected_componnent_map[root] is None:
            # New connected component
            number_connected_components += 1
            connected_componnent_map[root] = number_connected_components

        connected_componnent_map[node] = connected_componnent_map[root]
    return (connected_componnent_map, number_connected_components)

## REC
def connected_componnent_map_from_edges(number_nodes: int, node_pairs: list[tuple[int, int]]) -> tuple[list[int], int]:
    """Get the connected component for each node and the total number of connected componnents (recursively)
    from the list of edges and the number of nodes in a graph.
    """

    def __parent_aux(fathers: list[int], connected_componnent_map: list[int], node: int, number_connected_components: int) -> int:
        # Already found
        if connected_componnent_map[node] is not None:
            return connected_componnent_map[node]
        
        # Root (new connected component)
        if fathers[node] < 0:
            connected_componnent_map[node] = number_connected_components + 1
            return number_connected_components + 1
        
        updated = __parent_aux(fathers, connected_componnent_map, fathers[node], number_connected_components)
        connected_componnent_map[node] = updated
        return updated

    # Inline union_find
    fathers = [-1] * number_nodes
    for (node1, node2) in node_pairs:
        union(node1, node2, fathers)

    connected_componnent_map = [None] * number_nodes
    number_connected_components = 0

    # Get the connected components for each node recursively
    for node in range(number_nodes):
        if connected_componnent_map[node] is None:
            number_connected_components = max(number_connected_components, 
                                              __parent_aux(fathers, connected_componnent_map, node, number_connected_components))

    return (connected_componnent_map, number_connected_components)

### Warshall algorithm

## ITER
def to_matrix(self) -> list[list[int]]:
    """Get matrix of adjacency of graph G.
    """

    # Create
    matrix = [[0] * self.order for _ in range(self.order)]

    # Populate
    for node in range(self.order):
        for neigh in self.adjlists[node]:
            matrix[node][neigh] = 1

    return matrix

## ITER
def warshall(matrix: list[list[int]], order: int) -> list[list[int]]:
    """Run Warshall algorithm on matrix of adjacency of a graph.
    """

    for k in range(order):
        for i in range(order):
            if matrix[i][k]:
                for j in range(order):
                    matrix[i][j] = matrix[i][j] or matrix[k][j]
    return matrix

## ITER
def warshall_undirected(matrix: list[list[int]], order: int) -> list[list[int]]:
    """Run Warshall algorithm on matrix of adjacency of an undirected graph.
    """

    for k in range(order):
        for i in range(order):
            if matrix[i][k]:
                for j in range(order):
                    matrix[i][j] = matrix[i][j] or matrix[k][j]
                    matrix[j][i] = matrix[i][j]
    return matrix

## ITER
def connected_component_map_from_matrix_simple(matrix: list[list[int]]) -> tuple[list[int], int]:
    """Get the map of the connected component for each node of a graph using Warshall's algorithm on its adjacency matrix.
    """

    order = len(matrix)

    # Run Warshall algorithm
    matrix = warshall(matrix, order)

    connected_component_map = [0] * order
    number_connected_components = 0

    # Map each node to its connected component
    for node1 in range(order):
        for node2 in range(order):
            if matrix[node1][node2]:
                connected_component_map[node2] = number_connected_components
        number_connected_components += 1

    return (connected_component_map, number_connected_components)

## ITER
def connected_components_from_map(connected_component_map: list[int], number_connected_components) -> list[list[int]]:
    """Get the connected components from the connected component map and the number of connected components.
    """

    connected_components = [[] * number_connected_components]
    for node1, node2 in enumerate(connected_component_map):
        connected_components[node2].append(node1)
    return connected_components

## ITER
def connected_components_from_matrix(matrix: list[list[int]]) -> list[list[int]]:
    """Get the connected components of a graph using Warshall's algorithm on its adjacency matrix.
    """

    order = len(matrix)

    # Run Warshall algorithm
    matrix = warshall(matrix, order)

    connected_components = []
    number_connected_components = 0
    node = 0
    visited = [False] * order
    while number_connected_components < order:
        # New root
        if not visited[node]:
            componnent = [node]
            number_connected_components += 1

            # Add all nodes in connected component
            for y in range(node+1, order):
                if matrix[node][y]:
                    componnent.append(y)
                    visited[y] = True
                    number_connected_components += 1

            connected_components.append(componnent)
        node += 1
    return connected_components

## REC
def to_tree(self) -> list[int]:
    """Transforms the graph G into a tree in-place (recursively) and returns the map of its previously connected components.
    """

    def __make(G: graph.Graph, node: int, connected_component_map: list[int],
               number_connected_components: int, father: int, cycling_edges: list[int]):
        # Mark as ancestor for further recursive calls
        connected_component_map[node] = -number_connected_components

        for y in G.adjlists[node]:
            # New node
            if connected_component_map[y] is None:
                __make(G, y, connected_component_map, number_connected_components, node, cycling_edges)
            
            # Ancestor but not father
            elif y != father and connected_component_map[y] < 0:
                cycling_edges.append((node, y))
        
        # Unmark as ancestor
        connected_component_map[node] = number_connected_components

    connected_component_map = [None] * self.order
    number_connected_components = 1
    cycling_edges = []

    # Start with node 0 (tree root)
    __make(self, 0, connected_component_map, number_connected_components, -1, cycling_edges)

    # Then all other nodes
    for node in range(1, self.order):
        if connected_component_map[node] is None:
            # New local root
            number_connected_components += 1
            __make(self, node, connected_component_map, number_connected_components, -1, cycling_edges)
            
            # Link local root to tree root
            self.addedge(0, node)
    
    # Remove all cycles
    for (node1, node2) in cycling_edges:
        self.removeedge(node1, node2)
    
    return connected_component_map