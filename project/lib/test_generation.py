from generation import *
from test_equilibrium import cost_fn


def test_random_placements_returns_tuples():
    p = random_placements(10, 5)
    assert len(p) == 5
    assert type(p[0]) == tuple

def test_initial_state_is_mat_with_right_dims():
    state = initial_state([(1,3), (4,6)], 10)
    assert state.shape == (2,10,10)

    # both agents are on direct paths!
    assert state.sum() == 2

def test_remove_and_score_with_identity():
    state = initial_state([(1,3), (4,6)], 10)
    graph = fully_connected(10)
    score = remove_and_score((1,3), state, graph, lambda x,g: x*g)
    assert score == 3

def test_remove_and_score_with_inf_cost():
    state = initial_state([(1,3), (2,3)], 10)
    graph = fully_connected(10)
    score = remove_and_score((1,3), state, graph, cost_fn)
    assert score == 2

def test_score_edges():
    state = initial_state([(1,3), (2,3)], 10)
    graph = fully_connected(10)
    edges = score_edges(state, graph, cost_fn)
    assert np.all(np.array([e[0] for e in edges]) == 2.0) == True

def test_remove_best_edge_with_clear_fn():
    state = initial_state([(1,3), (2,3)], 4)
    graph = fully_connected(4)
    fn = lambda f,g: g*(.5)**(f - 1)
    new_graph = remove_best_edge(state, graph, fn)
    assert new_graph[1,3] == 0 or new_graph[2,3] == 0

def test_remove_best_edge_with_travelled_edge():
    state = initial_state([(1,3), (2,3)], 10)
    graph = fully_connected(10)
    new_graph = remove_best_edge(state, graph, cost_fn)
    assert new_graph[1,3] == 0 or new_graph[2,3] == 0

def test_find_optimum_subgraph():
    state = initial_state([(0,3), (1,3), (2,3)], 10)
    eps = .6
    graph = path_to_mat([(0,3,{'weight': 1}), (1,3, {'weight': 1}), (2,3, {'weight': 1}),
                         (4,3,{'weight': 1}), (0,4, {'weight': 1-eps}),
                         (1,4, {'weight': 1-eps}), (2,4,{'weight': 1-eps})],
                        10)
    new_graph = find_optimum_subgraph(state, graph, cost_fn, 10)
    print new_graph[0]
    assert new_graph[1][1,3] == 'foo'
