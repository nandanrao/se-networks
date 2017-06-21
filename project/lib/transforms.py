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
    m = np.nan_to_num(m)
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

def apply_nans(mat, nan_mat):
    """ MUTATES MAT -- makes that shit nan."""
    mat[np.isnan(nan_mat)] = np.nan
    return mat

def update_path(state, path, i):
    """ Updates the state with a new path for a given agent """
    N = state.shape[1]
    update = path_to_mat(path, N)
    s = np.copy(state)
    s[i,:,:] = update
    return apply_nans(s, state)

def get_potential_state(state, i):
    s = np.copy(state)
    s[i,:,:] = 1
    return s

def path_to_mat(path, N):
    a = np.zeros((N, N))
    for x,y in path:
        a[x,y] = 1
    return a

def get_distance(state, fn):
    flow = np.sum(state, axis=0)
    vfn = np.vectorize(fn, otypes=[np.float])
    distance = vfn(flow)
    return distance

def make_graph(dist):
    return nx.DiGraph(dist)

def get_shortest_path(dist, start, end):
    G = make_graph(dist)
    p = nx.dijkstra_path(G, start[0], end[1])
    return node_to_edge_list(p)

def get_next_path(state, i, fn):
    pot = get_potential_state(state, i)
    dist = get_distance(pot, fn)
    s,e = get_start_end(state, i)
    path = get_shortest_path(dist, s, e)
    new_state = update_path(state, path, i)
    return new_state

def find_equilibrium(state, fn):
    new_state = np.copy(state)
    for i in range(state.shape[0]):
        new_state = get_next_path(state, i, fn)
    if np.all(new_state == state):
        return state
    return find_equilibrium(new_state, fn)
