import py2neo
import igraph
import json
from py2neo import Graph as pGraph, authenticate
from igraph import Graph as iGraph

#Connect to Neo4j
authenticate("localhost:7474","neo4j", "BigData1")
neo4j = pGraph()

#Execute query to get data
query = "MATCH (p1:Paper)-[r:References]->(p2:Paper) RETURN p1.title, p2.title LIMIT 25"
data = neo4j.cypher.execute(query)

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
	d = {"id" : n.index, "title" : n["name"] , "cluster": communities.membership[n.index] }
	nodes.append(d)

#Output GraphJSON Format - http://graphalchemist.github.io/Alchemy/#/docs
graph_json = {"nodes":nodes, "edges":edges }
print json.dumps(graph_json)
