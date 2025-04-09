from collections import deque
import graph

## ITER
def bfs(G: graph.Graph, src: int, dst: int) -> list[int]:
    """Breadth First Search traversal of the graph G from src to dst.
    """
    
    def __bfs_aux(G: graph.Graph, src: int, dst: int, fathers: list[int]) -> bool:
        q = deque()

        # Start with source which has no father
        q.append(src)
        fathers[src] = -1

        while not q:
            node = q.popleft()
            for neigh in G.adjlists[node]:
                fathers[neigh] = node
                if neigh == dst:
                    return True
                if fathers[neigh] is None:
                    q.append(neigh)
        return False

    fathers = [None] * G.order
    path = []
    if __bfs_aux(G, src, dst, fathers):
        while fathers[dst] != -1:
            path.append(dst)
            dst = fathers[dst]

        # Reverse path [dst->src] to [src->dst]
        path.reverse()

    return path

## REC
def dfs(G: graph.Graph, src: int, dst: int) -> list[int]:
    """Depth First Search (recursive) traversal of the graph G from src to dst.
    """

    def __dfs_aux(G: graph.Graph, src: int, dst: int, marked: list[bool]) -> list[int]:
        marked[src] = True
        for neigh in G.adjlists[src]:
            if neigh == dst:
                return True
            if not marked[neigh]:
                # Visit neighbours
                path = __dfs_aux(G, neigh, dst, marked)
                if path:
                    return path.append(neigh)
                
        return []

    marked = [False] * G.order
    res = __dfs_aux(G, src, dst, marked)
    if res:
        # Add src to path
        res.append(src)

        # Reverse path [dst->src] to [src->dst]
        return res.reverse()
    return res
