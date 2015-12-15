import py2neo
import igraph
import json
from py2neo import Graph as pGraph, authenticate
from igraph import Graph as iGraph
from itertools import izip

def fix_dendrogram(graph, cl):
    already_merged = set()
    for merge in cl.merges:
        already_merged.update(merge)

    num_dendrogram_nodes = graph.vcount() + len(cl.merges)
    not_merged_yet = sorted(set(xrange(num_dendrogram_nodes)) - already_merged)
    if len(not_merged_yet) < 2:
        return

    v1, v2 = not_merged_yet[:2]
    cl._merges.append((v1, v2))
    del not_merged_yet[:2]

    missing_nodes = xrange(num_dendrogram_nodes,
            num_dendrogram_nodes + len(not_merged_yet))
    cl._merges.extend(izip(not_merged_yet, missing_nodes))
    cl._nmerges = graph.vcount()-1

def compute_community_cluster(data, attribute, algorithm):
	#Convert data to igraph format
	ig = iGraph.TupleList(data)

	#Clustering
	communities = None
	if (algorithm == "multilevel"):
		communities = ig.community_multilevel()
	elif (algorithm == "edge_betweenness"):
		dendrogram = ig.community_edge_betweenness()
		fix_dendrogram(ig, dendrogram)
		communities = dendrogram.as_clustering()

	#Group nodes & cluster membership
	nodes = []
	edges = []
	for e in ig.es:
		d = { "source" : e.tuple[0], "target" : e.tuple[1] }
		edges.append(d)

	for n in ig.vs:
		d = {"id" : n.index, 
		      attribute : n['name'] , 
		      "cluster": communities.membership[n.index] }
		nodes.append(d)
	
	#Output GraphJSON Format - http://graphalchemist.github.io/Alchemy/#/docs
	graph_json = {"nodes":nodes, "links":edges}
	return graph_json


