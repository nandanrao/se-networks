# problem 1

using LightGraphs
using GraphPlot
using Gadfly

edges = [0 1 1 0 0 0 0 0 0 0
         1 0 1 0 0 0 0 0 0 0
         1 1 0 1 1 0 0 0 0 0
         0 0 1 0 0 0 0 0 0 0
         0 0 1 0 0 1 1 1 1 0
         0 0 0 0 1 0 0 0 0 0
         0 0 0 0 1 0 0 0 0 1
         0 0 0 0 1 0 0 0 0 1
         0 0 0 0 1 0 0 0 0 1
         0 0 0 0 0 0 1 1 1 0]


g = Graph(edges)
gplot(g, nodelabel = degree(g))

plot(x = degree(g), Geom.histogram)

average_clustering(g) = sum(local_clustering_coefficient(g))/size(g)[1]

function average_distance(g)
    n = size(g)[1]
    pairs = n * (n - 1)
    sum(reduce(hcat, [gdistances(g, v) for v in vertices(g)]))/pairs
end


local_clustering_coefficient(g)
average_clustering(g)


average_distance(g)
diameter(g)

srand(123)
gplot(random_regular_graph(9, 2))
srand(126)
gplot(random_regular_graph(9, 2))



#####################################
# bipartite
b_edges = [0 0 0 0 0 0 1 0 0 0 0
           0 0 0 0 0 0 0 0 1 0 0
           0 0 0 0 0 0 1 1 1 0 0
           0 0 0 0 0 0 0 0 1 1 0
           0 0 0 0 0 0 0 0 1 0 1
           0 0 0 0 0 0 0 0 0 0 1
           1 0 1 0 0 0 0 0 0 0 0
           0 0 1 0 0 0 0 0 0 0 0
           0 1 1 1 1 0 0 0 0 0 0
           0 0 0 1 0 0 0 0 0 0 0
           0 0 0 0 1 1 0 0 0 0 0]

avg_degree(g) = mean(degree(g))

function get_proj(g)
    G = Graph(11)
    for v in vertices(g)
        d = gdistances(bg, v)
        i = find(x -> x == 2, d)
        [add_edge!(G, v, ind) for ind in i]
    end
    a,b = connected_components(G)
    G[a], G[b]
end

bg = Graph(b_edges)
a,b = get_proj(bg)

adjacency_matrix(a)
adjacency_matrix(b)


mean(degree(bg)[1:6])
mean(degree(bg)[7:11])


@test
