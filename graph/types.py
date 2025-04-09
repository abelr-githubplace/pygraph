import graph

## REC
def is_eulerian(self) -> bool:
    """Check (recursively) if graph G is eulerian.
    """

    def __is_eulerian(G: graph.Graph, src: int, marked: list[bool]) -> tuple[int, int]:
        # Visit src
        marked[src] = True
        degree = len(G.adjlists[src])
        number_odd = 0
        number_node = 1

        for neigh in G.adjlists[src]:
            # Remove self-looping nodes problem
            if src == neigh:
                degree += 1

            if not marked[neigh]:
                # Visit neighbours
                odd, n = __is_eulerian(G, neigh, marked)
                number_odd += odd
                number_node += n

                # Eulerian graph has less than 2 odd degree nodes
                if number_odd > 2:
                    return (number_odd, -1)
                
        number_odd += degree // 2
        return (number_odd, number_node)

    marked = [False] * self.order
    number_odd, number_node = __is_eulerian(self, 0, marked)

    # Eulerian graph has less than 2 odd degree nodes
    return number_odd <= 2 and number_node == self.order