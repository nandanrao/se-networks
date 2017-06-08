import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def network_from_df(path = "data/high-energy-trimmed.txt"):
    df = pd.read_csv(path)
    G = nx.DiGraph()
    df = pd.read_csv(path, sep="\t")
    nodes = df.iloc[:, 1].unique().tolist()
    edges = [(f[0], f[1]) for f in df.as_matrix()]
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    return G


# 2

# A
hits = nx.hits_scipy(g)
pagerank = nx.pagerank_scipy(g)# default .85
eigen = nx.eigenvector_centrality(g)
degree = nx.degree_centrality(g)

get_top_hubs = lambda hits: get_top_nodes(hits[0])
get_top_auths = lambda hits: get_top_nodes(hits[1])

def get_top_nodes(d, n = 20):
    return map(lambda x: x[0],
               sorted(d.items(), key=lambda x: x[1]))[0:n]

get_top_nodes(degree)
get_top_nodes(eigen)
get_top_nodes(pagerank)
get_top_hubs(hits)
get_top_auths(hits)


# B

g = nx.erdos_renyi_graph(50, 0.1)

sns.distplot(g.degree().values())
