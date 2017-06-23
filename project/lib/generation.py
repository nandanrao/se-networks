# cycle through run dijkstras based on... graph of ones? that'll do.
# then start removing edges...
# cycle through removing each edge, finding equilibrium, and adding up costs.
# cost is just distance matrix... added??? somehow avoid cost functions

import numpy as np
from equilibrium import *
from multiprocessing import Pool

def mc_map(fn, dat):
    pool = Pool(multiprocessing.cpu_count() - 1)
    ans = pool.map(fn, dat)
    pool.close()
    return ans

def random_placements(N, A):
    raw_choices = [np.random.choice(range(N), 2, False) for _ in range(A)]
    return map(tuple, raw_choices)

def fully_connected(N):
    return np.ones((N,N))

def initial_state(agents, dist):
    """ Creates initial state

    :param agents: list of tuples with start/finish nodes
    :param dist: adjacency matrix of initial graph
    """
    N = dist.shape[1]
    edge_lists = [get_shortest_path(dist,s,f) for s,f in agents]
    state = np.stack([path_to_mat(p, N) for p in edge_lists])
    return state

def remove_edge(e, graph):
    g = np.copy(graph)
    g[e] = 0
    return g

def apply_on_tensor(arr, fn):
    """ fn which takes a matrix and returns a matrix"""
    return np.array([fn(arr[i,:,:]) for i in range(arr.shape[0])])

def score_graph(state, graph, fn):
    dist = get_distance(state, graph, fn)
    # TODO: this is ugly.
    d =  apply_on_tensor(state, lambda s: s*dist)
    return np.nan_to_num(d).sum()

def remove_and_score(e, state, graph, fn):
    new_graph = remove_edge(e, graph)
    try:
        new_state = find_equilibrium(state, new_graph, fn)
        return score_graph(new_state, new_graph, fn)
    except nx.exception.NetworkXNoPath:
        return float('inf') # some node not reachable

class RemovingScorer(object):
    def __init__(self, state, graph, fn):
        self.state = state
        self.graph = graph
        self.fn = fn
    def __call__(self, edge):
        return (remove_and_score(edge, self.state, self.graph, self.fn), edge)

def score_edges(state, graph, fn):
    N = state.shape[1]
    G = make_graph(graph)
    edges = list(G.edges())
    scored_edges = mc_map(RemovingScorer(state, graph, fn), edges)
    return sorted(scored_edges, key = lambda t: t[0])


def get_travelled_edges(state):
    return list(make_graph(state.sum(axis=0)).edges())

def get_best_edge(state, graph, fn):
    edges = score_edges(state, graph, fn)
    travelled_edges = get_travelled_edges(state)
    edges = [e for e in edges if e[1] in travelled_edges]
    # best_edges = [e for e in edges if e[0] == edges[0][0]]
    # prefer to return a travelled edge if possible
    # print edges
    # for e in best_edges:
        # if e[1] in travelled_edges:
            # return e[1]
    return edges[0][1]

def remove_best_edge(state, graph, fn):
    edges = get_best_edge(state, graph, fn)
    if type(edges) == list:
        graph = reduce(lambda g,e: remove_edge(e, g), edges, graph)
    else:
        graph = remove_edge(edges, graph)
    return graph

def find_optimum_subgraph(state, graph, fn, i=100):
    """

    :returns: a tuple with (score, graph)
    """
    score = score_graph(state, graph, fn)
    scored = [(score, graph)]

    # remove cruft from grpah??
    best = lambda : sorted(scored, key = lambda x: x[0])[0]
    while i > 0:
        new_graph = remove_best_edge(state, graph, fn)
        if np.all(new_graph == graph):
            return best()
        try:
            state = find_equilibrium(state, new_graph, fn)
        except nx.exception.NetworkXNoPath:
            return best()
        score = score_graph(state, new_graph, fn)
        scored.append((score, new_graph))
        graph = new_graph
        i = i-1
    return best()

class Scorer(object):
    def __init__(self, state, fn):
        self.state = state
        self.fn = fn
    def __call__(self, graph):
        return get_equilibrium_score(self.state, graph, self.fn)

def combinatorial_optimum(state, graphs, fn):
    scores = mc_map(Scorer(state, fn), graphs)
    return sorted(zip(scores, graphs), key = lambda x: x[0])[0]

def get_equilibrium_score(state, graph, fn):
    try:
        equilibrium_state = find_equilibrium(state, graph, fn)
        return score_graph(equilibrium_state, graph, fn)
    except nx.NetworkXNoPath:
        return float('inf')

def combinations(els, curr = []):
    """ returns list of lists with combinations of element in og list"""
    if len(els) == 1:
        return [curr + els] + [curr]
    return combinations(els[1:], curr + els[:1])+ combinations(els[1:], curr)

# mvove to notebook?
def random_distances(graph):
    n = graph.shape[0]
    rands = np.ceil((np.random.power(.15, n**2).reshape((n,n)) * 10))
    return graph * rands
