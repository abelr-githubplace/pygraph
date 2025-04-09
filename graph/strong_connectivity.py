from collections import deque
import graph

## ITER
def reverse(self) -> graph.Graph:
    """Get reversed graph of graph G.
    """

    revG = graph.Graph(self.order, True)
    for i in range(self.order):
        for y in self.adjlists[i]:
            revG.add_edge(y, i)

## REC
def kosaraju(self) -> tuple[list[int], int]:
    """Get the map of strongly connected component for each node and
    the number of strongly connected components of graph G using Kosaraju's algorithm.
    """

    def __dfs(G: graph.Graph, node: int, marked: list[any], mark: any = True):
        marked[node] = mark
        for neigh in G.adjlists[node]:
            if not marked[neigh]:
                __dfs(G, neigh, marked, mark)
    
    
    def __dfs_suff(G: graph.Graph, x: int, M: list[int], suff: deque):
        M[x] = True
        for y in G.adjlists[x]:
            if not M[y]:
                __dfs_suff(G, y, M, suff)
        suff.append(x)

    suffix_order = deque()
    marked = [False] * self.order
    # Get suffix order
    for node in range(self.order):
        if not marked[node]:
            __dfs_suff(self, node, marked, suffix_order)
    
    # Get reversed graph
    revG = self.reverse()
    number_strongly_connected_components = 0
    strongly_connected_component_map = [False] * self.order
    # Get strongly connected components
    while not suffix_order.isempty():
        node = suffix_order.pop()
        if not strongly_connected_component_map[node]:
            number_strongly_connected_components += 1
            __dfs(revG, node, strongly_connected_component_map, number_strongly_connected_components)
    return (strongly_connected_component_map, number_strongly_connected_components)

## REC
def tarjan(self) -> tuple[list[int], int]:
    """Get the map of strongly connected component for each node and
    the number of strongly connected components of graph G using Tarjan's algorithm.
    """

    def __tarjan_aux(G: graph.Graph, node: int, prefix_index: list[int],
                     counter: int, strongly_connected_component_map: list[int],
                     number_strongly_connected_components: int, stack: deque) -> tuple[int, int, int]:
        stack.append(node)
        counter += 1
        prefix_index[node] = counter
        return_value = counter

        # Recursively add nodes to component and minimize return value
        for neigh in G.adjlists[node]:
            if prefix_index[neigh] == 0:
                return_y, counter, number_strongly_connected_components = __tarjan_aux(G, neigh, prefix_index, counter,
                                                                                       strongly_connected_component_map,
                                                                                       number_strongly_connected_components, stack)
                return_value = min(return_value, return_y)
            else:
                return_value = min(return_value, prefix_index[neigh])

        # Return value not minimized means we found the root of a component
        if return_value == prefix_index[node]:
            number_strongly_connected_components += 1
            neigh = -1 # Not a valid node
            while neigh != node: # Stack empty after last call (root of tree is root of component)
                neigh = stack.pop()
                strongly_connected_component_map[neigh] = number_strongly_connected_components
                prefix_index[neigh] = G.order
        
        return (return_value, counter, number_strongly_connected_components)


    stack = deque()
    prefix_index = [0] * self.order
    strongly_connected_component_map = [0] * self.order
    number_strongly_connected_components = 0
    counter = 0

    # Get strongly connected components of all roots
    for node in range(self.order):
        if prefix_index[node] == 0:
            (_, counter, number_strongly_connected_components) = __tarjan_aux(self, node, prefix_index, counter,
                                                                              strongly_connected_component_map,
                                                                              number_strongly_connected_components, stack)

    return (strongly_connected_component_map, number_strongly_connected_components)