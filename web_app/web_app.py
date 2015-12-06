import scholarly
from py2neo import Graph as pGraph, authenticate
from flask import Flask, render_template, url_for

app = Flask(__name__)

authenticate("localhost:7474","neo4j", "BigData1")
neo4j = pGraph()


@app.route("/")
def hello():
	return render_template("index.html")

@app.route("/papers/cluster/<int:limit>")
def paper_clusters(limit):
	query = "MATCH (p1:Paper)-[r:References]->(p2:Paper) RETURN p1.title, p2.title LIMIT %d" % (limit)
	
	data = neo4j.cypher.execute(query)
	graph_json = scholarly.compute_community_cluster(data, "title")
	
	return graph_json

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8888)

