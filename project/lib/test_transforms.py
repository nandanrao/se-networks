from transforms import *
import networkx as nx
import random

def test_get_distance_applies_function():
    paths = [[(1,2), (2,3), (3,6)], [(2,3), (3,6), (6,9)]]
    state = np.stack([path_to_mat(p, 10) for p in paths])
    fn = lambda f: 1/f if f > 0 else float('inf')
    d = get_distance(state, fn)
    assert d[2,3] == .5
    assert d[1,2] == 1
    assert d[0,0] == float('inf')

def test_get_potential_state():
    paths = [[(1,2), (2,3), (3,4)], [(2,3), (3,4)]]
    state = np.stack([path_to_mat(p, 5) for p in paths])

    # make sure it works with nan's
    state[1,1] = np.nan
    new_state = get_potential_state(state, 1)

    # check that there are no zeros on any edge
    assert np.any(np.sum(new_state, axis=0) == 0) == False

def test_update_path():
    paths = [[(1,2), (2,3), (3,4)], [(2,3), (3,4)]]
    state = np.stack([path_to_mat(p, 5) for p in paths])
    state[0,0,0] = np.nan
    new_state = update_path(state, [(2,3), (3,1)], 1)

    assert np.isnan(new_state[0,0,0])
    assert new_state[1,2,3] == 1
    assert new_state[1,3,1] == 1
    assert new_state[1,3,4] == 0

def test_apply_nans():
    nan_mat = np.array([[np.nan, 1.], [2.,3.]])
    mat = np.array([[3.,4.], [5.,6.]])
    applied = apply_nans(mat, nan_mat)
    assert np.isnan(applied[0,0])
    assert applied[1,1] == 6

# def test_get_path():
#     paths = [[(1,2), (2,3), (3,4)], [(2,3), (3,4)]]
#     state = np.stack([path_to_mat(p, 5) for p in paths])
#     assert get_path(state, 0) == [(1,2), (2,3), (3,4)]

def test_start_end_a():
    s = [(9,7), (7,2), (2,8), (8,1)]
    m = path_to_mat(s, 10)
    m[0,0] = np.nan
    assert start_end(m) == (9,1)

    # Make sure it's not fluke
    s = [(1,7), (7,2), (2,8), (8,9)]
    m = path_to_mat(s, 10)
    m[0,0] = np.nan
    assert start_end(m) == (1,9)

def test_get_start_end():
    paths = [[(1,2), (2,3), (3,4)], [(2,3), (3,4)]]
    state = np.stack([path_to_mat(p, 5) for p in paths])
    assert get_start_end(state, 1) == ((2,3), (3,4))

def test_start_end_a():
    s = [(9,7), (7,2), (2,8), (8,1)]
    m = path_to_mat(s, 10)
    m[0,0] = np.nan
    assert start_end(m) == (9,1)

    # Make sure it's not fluke
    s = [(1,7), (7,2), (2,8), (8,9)]
    m = path_to_mat(s, 10)
    m[0,0] = np.nan
    assert start_end(m) == (1,9)

def test_arrange_path():
    s = [(9,7), (7,2), (2,8), (8,1)]
    m = path_to_mat(s, 10)
    m[0,0] = np.nan
    assert arrange_path(m, [9]) == [(9,7), (7,2), (2,8), (8,1)]

def test_node_to_edge_list():
    assert node_to_edge_list([1,2,3,4,5]) == [(1,2), (2,3), (3,4), (4,5)]

def test_get_next_path():
    paths = [[(1,2), (2,3), (3,4)], [(2,3), (3,4)]]
    state = np.stack([path_to_mat(p, 5) for p in paths])
    fn = lambda f: 1/f if f > 0 else float('inf')
    new_state = get_next_path(state, 0, fn)

    # TODO: properly test and make a real assertion...
    assert np.all(new_state == state) == False

def test_find_equilibrium():
    paths = [[(1,2), (2,3), (3,4)], [(2,3), (3,4)], [(2,3), (3,4)]]
    state = np.stack([path_to_mat(p, 5) for p in paths])
    fn = lambda f: 1/f if f > 0 else float('inf')
    new_state = find_equilibrium(state, fn)

    # TODO: properly test and make a real assertion...
    assert np.all(new_state == state) == True
