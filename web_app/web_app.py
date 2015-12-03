import py2neo
import igraph
import json
from py2neo import Graph as pGraph, authenticate
from igraph import Graph as iGraph
from flask import Flask

app = Flask(__name__)

authenticate("localhost:7474","neo4j", "BigData1")
neo4j = pGraph()


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
		      attribute : n[attribute] , 
		      "cluster": communities.membership[n.index] }
		nodes.append(d)

	#Output GraphJSON Format - http://graphalchemist.github.io/Alchemy/#/docs
	graph_json = {"nodes":nodes, "edges":edges }
	return json.dumps(graph_json)

@app.route("/")
def hello():
	return "Hello World!"

@app.route("/papers/cluster/<int:limit>")
def paper_clusters(limit):
	query = "MATCH (p1:Paper)-[r:References]->(p2:Paper) RETURN p1.title, p2.title LIMIT %d" % (limit)
	
	data = neo4j.cypher.execute(query)
	graph_json = compute_community_cluster(data, "title")
	
	return graph_json

if __name__ == "__main__":
	app.run(host='0.0.0.0')
