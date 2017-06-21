import networkx as nx
from toolz import assoc

def simple_path(path):
    return ((e[0], e[1]) for e in path)

def edge_in_path(e, p):
    return (e[0], e[1]) in simple_path(p)

def inc_attr(e, attr, amt):
    return e[0], e[1], { attr: e[2][attr]+amt }

def inc_graph(G, path, attr, amt):
    edges = G.edges(data=True)
    G.add_edges_from([inc_attr(e, attr, amt)
                      for e in edges if edge_in_path(e, path)])
    return G

def potential_network(G, path):
    """ Returns the network as seen by an agent with path p. """
    edges = list(G.edges()) # make list because we iterate it twice
    to_explore = [e for e in edges if e not in path]
    return inc_graph(G, to_explore, 'flow', 1)

def calc_weight(fn, e):
    return e[0], e[1], assoc(e[2], 'weight', fn(e[2]['flow']))

def compute_distance(G, fn):
    """ Calculates edge weights based on flow and flow function fn """
    edges = G.edges(data=True)
    G.add_edges_from([calc_weight(fn, e) for e in edges])
    return G

def update_graph_with_path(G, old_path, new_path):
    G = inc_graph(G, old_path, 'flow', -1)
    G = inc_graph(G, new_path, 'flow', 1)
    return G

def get_path(A):
    """ Returns current path for given agent """
    return A

def find_new_path(G, A, fn):
    """ Returns new graph and agent with new best path."""
    path = get_path(A)
    fov = potential_network(G, path)
    compute_distance(G, fn)
    shortest_path = nx.dijkstra_path(G, path)
    new_G = update_graph_with_path(G, opath, shortest_path)
    new_A = update_agent(A, new_path)
    return new_G, new_A
