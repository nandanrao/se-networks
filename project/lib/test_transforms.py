from transforms import *
import networkx as nx

def basic_G():
    G = nx.DiGraph()
    G.add_nodes_from([1,2,3])
    G.add_edges_from([(1,2), (1,3)], flow = 1)
    G.add_edges_from([(2,3)], flow = 0)
    return G

def test_edge_in_path():
    G = basic_G()
    assert edge_in_path((1,2), G.edges(data=True)) == True
    assert edge_in_path((1,2), G.edges()) == True
    assert edge_in_path((1,2,{'flow': 1}),  G.edges(data=True)) == True
    assert edge_in_path((1,2,{'flow': 1}), G.edges()) == True

def test_potential_network_adds_edge_weights():
    G = basic_G()
    p = [(1,2), (1,3)]
    new_G = potential_network(G, p)
    inverted = list(new_G.edges(data = True))
    assert map(lambda t: t[2]['flow'], inverted) == [1,1,1]

def test_compute_distance_applies_function():
    G = basic_G()
    fn = lambda f: 1/f if f > 0 else float('inf')
    with_weights = list(compute_distance(G, fn).edges(data=True))
    assert map(lambda t: t[2]['weight'], with_weights) == [1,1,float('inf')]

def test_update_graph_with_path():
    G = nx.DiGraph()
    G.add_nodes_from([1,2,3,4])
    G.add_edges_from([(1,2), (1,3), (3,4), (4,1)], flow = 1)
    G.add_edges_from([(2,3)], flow = 0)
    old_path = [(1,2), (1,3)]
    new_path = [(1,2), (2,3), (3,4)]
    ug = update_graph_with_path(G, old_path, new_path)
    edges = list(ug.edges(data=True))
    expected = [(1,2, {'flow': 1}), (1,3, {'flow': 0}), (3,4, {'flow': 2}), (4,1,{'flow': 1}), (2,3, {'flow': 1})]
    assert sorted(edges, key = lambda x: x[0]) == sorted(expected, key = lambda x: x[0])
