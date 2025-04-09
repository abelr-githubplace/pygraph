"""Simple graph module.

Provide an implementation of graphs with adjacency lists.

Terminology used:
    A graph is made of nodes and (directed or undirected) edges.
    The order of the graph is the number of its nodes (ranging from zero to order minus one).

The node number can then be used to access its adjacency list.

"""


class Graph:
    """ Simple class for graph: adjacency lists

    Attributes:
        order (int): Number of nodes.
        directed (bool): True if the graph is directed. False otherwise.
        adjlists (List[List[int]]): Lists of connected nodes for each node.
        labels (list[str]): optionnal vector of node labels
        costs (dict): [optionnal] edge (src, dst) -> cost (float)
        
    """

    from .traversal import dfs, bfs
    from .order import topological_order
    from .colored import is_colored_nicely
    from .types import is_eulerian
    from .subgraph import build_subgraph
    from .connectivity import to_matrix, to_tree
    from .strong_connectivity import kosaraju, tarjan, reverse
    

    def __init__(self, order, directed=False, costs=False, labels=None):
        """Init graph, allocate adjacency lists

        Args:
            order (int): Number of nodes.
            directed (bool): True if the graph is directed. False otherwise.
            labels (list[str]): optionnal vector of node labels
            costs (bool): True if the graph is weighted. False otherwise. 

        """

        self.order = order
        self.directed = directed
        if costs:
            self.costs = {}
        else:
            self.costs = None
        self.adjlists = []
        for _ in range(order):
            self.adjlists.append([])
        self.labels = labels


    def add_edge(self, src, dst, cost=None):
        """Add egde to graph.
    
        Args:
            src (int): Source node.
            dst (int): Destination node.
            cost: if not None, the cost of edge (src, dst)
    
        Raises:
            IndexError: If any node index is invalid.
    
        """
    
        # Check node indices.
        if src >= self.order or src < 0:
            raise IndexError("Invalid src index")
        if dst >= self.order or dst < 0:
            raise IndexError("Invalid dst index")

        self.adjlists[src].append(dst)
        if not self.directed and dst != src:
            self.adjlists[dst].append(src)
        if self.costs is not None:
            self.costs[(src, dst)] = cost
            if not self.directed:
                self.costs[(dst, src)] = cost


    def add_node(self, number=1, labels=None):
        """Add number nodes to graph.
    
        Args:
            ref (Graph).
            number (int): Number of nodes to add.
            labels (str list)optionnal list of new node labels
    
        """
    
        # Increment order and extend adjacency list
        self.order += number
        for _ in range(number):
            self.adjlists.append([])
        if labels:
            self.labels += labels

    def remove_edge(self, src, dst):
        """Remove egde from the graph.
    
        Args:
            src (int): Source node.
            dst (int): Destination node.
    
        Raises:
            IndexError: If any node index is invalid.
            
        """

        if src >= self.order or src < 0:
            raise IndexError("Invalid src index")
        if dst >= self.order or dst < 0:
            raise IndexError("Invalid dst index")
        if dst in self.adjlists[src]:
            self.adjlists[src].remove(dst)
            if self.costs:
                self.costs.pop((src, dst))
            if not self.directed and dst != src:
                self.adjlists[dst].remove(src)
                if self.costs:
                    self.costs.pop((dst, src))

def sort(G):
    """
    sorts adjacency lists
    """
    for i in range(G.order):
        G.adjlists[i].sort()
        
                    
def dot(G):
    """Dot format of graph.

    Args:
        Graph

    Returns:
        str: String storing dot format of graph.

    """

    if G.directed:
        s = "digraph {\n"
        for x in range(G.order):
            if G.labels:
                s += "  " + str(x) + '[label = "' + G.labels[x] + '"]\n'
            else:
                s += "  " + str(x) + '\n'
            for y in G.adjlists[x]:
                cost = ' [label=' + str(G.costs[(x, y)]) + '] ' if G.costs else ""
                s += str(x) + " -> " + str(y) + cost + '\n'
    else:
        s = "graph {\n"
        for x in range(G.order):
            if G.labels:
                s += "  " + str(x) + '[label = "' + G.labels[x] + '"]\n'
            else:
                s += "  " + str(x) + '\n'
            for y in G.adjlists[x]:
                if x <= y:
                    cost = ' [label=' + str(G.costs[(x, y)]) + '] ' if G.costs else ""
                    s += str(x) + " -- " + str(y) + cost + '\n'    
  
    s += "}"
    return s


def display(G, eng=None):
    """
    *Warning:* Made for use within IPython/Jupyter only.
    eng: graphivz.Source "engine" optional argument (try "neato", "fdp", "sfdp", "circo")
    
    """
    
    try:
        from graphviz import Source
        from IPython.display import display
    except:
        raise Exception("Missing module: graphviz and/or IPython.")
    display(Source(dot(G), engine=eng))


# load / save gra format    

def load(filename):
    """Build a new graph from a GRA file.

    Args:
        filename (str): File to load.

    Returns:
        Graph: New graph.

    Raises:
        FileNotFoundError: If file does not exist. 

    """

    f = open(filename)
    lines = f.readlines()
    f.close()
    
    infos = {}
    i = 0
    while '#' in lines[i]:
        (key, val) = lines[i][1:].strip().split(": ")
        infos[key] = val
        i += 1

    directed = bool(int(lines[i]))
    order = int(lines[i+1])

    if infos and "labels" in infos:
        labels = infos["labels"].split(',') #labels is a list of str
        G = Graph(order, directed, labels)  # a graph with labels
    else:
        G = Graph(order, directed)  # a graph without labels
    if infos:
        G.infos = infos
    
    for line in lines[i+2:]:
        edge = line.strip().split(' ')
        (src, dst) = (int(edge[0]), int(edge[1]))
        G.add_edge(src, dst)
    return G

def load_weightedgraph(filename, costType=float):
    """Build a new weighted graph from a WGRA file.

    Args:
        filename (str): File to load.

    Returns:
        Graph: New graph.
    """
    f = open(filename)
    lines = f.readlines()
    infos = {}
    i = 0
    while '#' in lines[i]:
        (key, val) = lines[i][1:].strip().split(": ")
        infos[key] = val
        i += 1
    directed = bool(int(lines[i]))
    order = int(lines[i+1])
    G = Graph(order, directed, costs=True)
    G.infos = infos
    if G.infos and "labels" in G.infos:
        G.labels = G.infos["labels"].split(',')    
    for line in lines[i+2:]:
        edge = line.strip().split(' ')
        (x, y, cost) = (int(edge[0]), int(edge[1]), costType(edge[2]))
        G.add_edge(x, y, cost)
    f.close()

    return G
    
def save(G, fileOut):
    gra = ""
    if G.labels:
        lab = "#labels: "
        for i in range(G.order - 1):
            lab += G.labels[i] + ','
        lab += G.labels[-1]
        gra += lab + '\n'
    gra += str(int(G.directed)) + '\n'
    gra += str(G.order) + '\n'
    for x in range(G.order):
        for y in G.adjlists[x]:
            if G.directed or x >= y:
                cost = ' ' + str(G.costs[(x, y)]) if G.costs else ""
                gra += str(x) + " " + str(y) + cost + '\n'
    fout = open(fileOut, mode='w')
    fout.write(gra)
    fout.close()
