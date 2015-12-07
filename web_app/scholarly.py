import py2neo
import igraph
import json
from py2neo import Graph as pGraph, authenticate
from igraph import Graph as iGraph

def compute_community_cluster(data, attribute):
	#Convert data to igraph format
	ig = iGraph.TupleList(data)

	#Clustering
	communities = ig.community_multilevel()

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


