import scholarly
import json
import urllib
from py2neo import Graph as pGraph, authenticate
from flask import Flask, render_template, url_for

app = Flask(__name__)

authenticate("localhost:7474","neo4j", "BigData1")
neo4j = pGraph()


@app.route("/")
def main():
	return render_template("index.html")

@app.route("/clustering")
def clustering():
	return render_template("cluster.html")

@app.route("/analytics")
def analytics():
	return render_template("analytics.html")

@app.route("/papers/cluster/<int:limit>")
def paper_clusters(limit):
	query = "MATCH (p1:Paper)-[r:Wrote]->(p2:Paper) RETURN p1.title, p2.title LIMIT %d" % (limit)
	
	data = neo4j.cypher.execute(query)
	graph_json = scholarly.compute_community_cluster(data, "title")

	return json.dumps(graph_json)

@app.route("/papers/cluster/<int:limit>/<keyword>")
def paper_clusters_keyword(limit, keyword):
        query = "MATCH (p1:Paper)-[r:References]->(p2:Paper) WHERE p1.title CONTAINS '%s' RETURN p1.title, p2.title LIMIT %d" % (keyword, limit)
	
	query_alt = "MATCH (p1:Paper)<-[:Wrote]-(a:Author)-[a:Wrote]->(p2:Paper) WHERE p1.title CONTAINS '%s' RETURN p1,a, p2 LIMIT %d" % (keyword, limit)

        data = neo4j.cypher.execute(query)
        graph_json = scholarly.compute_community_cluster(data, "title")

        return json.dumps(graph_json)

@app.route("/papers/cluster/<int:limit>/cluster/<int:clusterId>")
def paper_clusters_cluster_info(limit, clusterId):
	query = "MATCH (p1:Paper)-[r:References]->(p2:Paper) RETURN p1.title, p2.title LIMIT %d" % (limit)
	
	data = neo4j.cypher.execute(query)
	graph_dict = scholarly.compute_community_cluster(data, "title")

	papers_in_cluster = []
	for n in graph_dict["nodes"]:
		if (n["cluster"] == clusterId):
			papers_in_cluster.append({"title" : n["title"], 
			"url" : "http://dblp.uni-trier.de/search/publ?q=" + urllib.quote(n["title"])})

	return render_template("cluster_info.html", data=papers_in_cluster);

@app.route("/top/<category>/<int:limit>")
def get_top(category, limit):
	query = None
	query_data = []

	if (category == "reference"):
		query = "MATCH (paper1:Paper)-[r:References]->(paper2:Paper) RETURN paper2.title as title, paper2.abstract as abstract, paper2.year as year, paper2.venue as venue, count(r) as num ORDER BY count(r) DESC LIMIT %d" % (limit)
		data = neo4j.cypher.execute(query)
		for paper in data:
			query_data.append( { "Title" : paper.title, "Venue" : paper.venue, "Year" : paper.year, "Abstract" : paper.abstract, "RefNum" : paper.num } )
	elif (category == "author"):
		query = "MATCH (author:Author)-[r:Wrote]->(paper:Paper) RETURN author.keyterms as keyterms, author.name as name, count(r) as num ORDER BY count(r) DESC LIMIT %d" % (limit)
		data = neo4j.cypher.execute(query)
		for author in data:
			query_data.append( { "AuthorName" : author.name, "Keyterms" : author.keyterms, "PublishNum" : author.num } )
	elif (category == "institute"):
		query = "MATCH (p:Paper)<-[w:Wrote]-(author:Author)-[r:Affiliated]->(institute:Institute) RETURN institute.` name` as name, count(w) as num ORDER BY count(w) DESC LIMIT %d" % (limit)
		data = neo4j.cypher.execute(query)
		for institute in data:
			query_data.append( { "InstituteName" : institute.name, "PublishNum" : institute.num } )

	return json.dumps(query_data)	

 
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8801)

