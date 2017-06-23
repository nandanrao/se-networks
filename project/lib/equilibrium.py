import networkx as nx
import numpy as np

def get_path(m):
    """ returns matrix path in list of tuples format"""
    s,f = start_end(m)
    return arrange_path(m, [s])

def node_to_edge_list(l):
    """ Takes a list of nodes and turns into a list of edges """
    fn = lambda a,b: a + [(a[-1][1], b)]
    return reduce(fn, l[2:], [(l[0], l[1])])

def get_end(m,i):
    return np.nonzero(m[i,:] == 1)[0][0]

def arrange_path(m, ordered):
    """ assumes no self loops! """
    while True:
        e = ordered[-1]
        try:
            # get the column of the non-zero element of this row
            # this will throw if there is none, showing we're done.
            n = get_end(m,e)
            ordered.append(n)
        except IndexError:
            return node_to_edge_list(ordered)

def sorted_path(m):
    """ Sorted path in order of travel """
    s,f = start_end(m)
    return path

def start_end(m):
    """ start and end node of path matrix """
    a,b = m.sum(axis=1), m.sum(axis=0)
    summed = a + b
    s,f =  np.nonzero(summed == 1)[0]
    if np.any(s  == np.nonzero(b == 1)):
        s,f = f,s
    return s,f

def get_start_end(state, i):
    """ Returns start and end node of an agent """
    m = state[i,:,:]
    p = get_path(m)
    return (p[0], p[-1])

def update_path(state, path, i):
    """ Updates the state with a new path for a given agent """
    N = state.shape[1]
    update = path_to_mat(path, N)
    s = np.copy(state)
    s[i,:,:] = update
    return s

def get_potential_state(state, i):
    s = np.copy(state)
    s[i,:,:] = 1
    return s

def path_to_mat(path, N):
    a = np.zeros((N, N))
    try:
        for x,y,v in path:
            a[x,y] = v['weight']
    except ValueError:
        for x,y in path:
            a[x,y] = 1
    return a

def get_distance(state, graph, fn):
    flow = np.sum(state, axis=0)
    it = np.nditer([flow, graph, None])
    for f,g,o in it:
        # Distance is 0 if edge not in graph!
        o[...] = 0 if g == 0 else fn(f,g)
    return it.operands[2]

def make_graph(dist):
    return nx.DiGraph(dist)

def get_shortest_path(dist, start, end):
    # Accept edge pairs or node indices
    if type(start) == tuple:
        start = start[0]
        end = end[1]
    G = make_graph(dist)
    p = nx.dijkstra_path(G, start, end)
    return node_to_edge_list(p)

def get_next_path(state, graph, i, fn):
    pot = get_potential_state(state, i)
    dist = get_distance(pot, graph, fn)
    s,e = get_start_end(state, i)
    path = get_shortest_path(dist, s, e)
    new_state = update_path(state, path, i)
    return new_state

def find_equilibrium(state, graph, fn):
    new_state = np.copy(state)
    reducer = lambda s,i: get_next_path(s, graph, i, fn)
    new_state = reduce(reducer, range(state.shape[0]), new_state)
    if np.all(new_state == state):
        return state
    return find_equilibrium(new_state, graph, fn)
