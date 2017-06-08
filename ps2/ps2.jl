using LightGraphs
using GraphPlot
using Gadfly
using DataFrames


dat = readtable("data/high-energy-trimmed.txt", separator='\t')

function create_graph_from_df()
    a = convert(Array, dat)
    nodes = unique(a[:,1])
    N = size(nodes)[1]
    lookup = Dict(collect(zip(nodes, collect(1:N))))
    g = DiGraph(N)
    d = [get(lookup, x, 1) for x in a]
    [add_edge!(g, d[i,:][1], d[i,:][2]) for i in 1:size(d)[1]]
    g
end

g = erdos_renyi(5000, 0.01)
