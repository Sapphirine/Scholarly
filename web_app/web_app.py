import scholarly
import json
import urllib
from py2neo import Graph as pGraph, authenticate
from py2neo.packages.httpstream import http
from flask import Flask, render_template, url_for

http.socket_timeout = 9999

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

@app.route("/papers/cluster/<algorithm>/<int:limit>")
@app.route("/papers/cluster/<algorithm>/<int:limit>/<keyword>")
def paper_clusters(algorithm, limit, keyword=""):

        query = None
        if (keyword == ""):
                query = "MATCH (p1:Paper)-[r:References]->(p2:Paper) RETURN p1.title, p2.title LIMIT %d" % (limit)
        else:
                query = "MATCH (p1:Paper)-[r:References]->(p2:Paper) WHERE p1.title CONTAINS '%s' OR p2.title CONTAINS '%s' RETURN p1.title, p2.title LIMIT %d" % (keyword, keyword, limit)

        print query
        data = neo4j.cypher.execute(query)
        graph_json = scholarly.compute_community_cluster(data, "title", algorithm)

        return json.dumps(graph_json)
@app.route("/authors/cluster/<algorithm>/<int:limit>")
@app.route("/authors/cluster/<algorithm>/<int:limit>/<keyword>")
def author_clusters(algorithm, limit, keyword=""):
	
	query = None
	if (keyword == ""):
		query = "MATCH (a1:Author)-[:Wrote]-(p:Paper)-[:Wrote]-(a2:Author) RETURN a1.name AS source, a2.name AS target LIMIT %d" % (limit)
	else:
		query = "MATCH (a1:Author)-[:Wrote]-(p:Paper)-[:Wrote]-(a2:Author) WHERE '%s' IN a1.keyterms AND '%s' IN a2.keyterms RETURN a1.name AS source, a2.name AS target LIMIT %d" % (keyword, keyword, limit)
	
	print query	
	data = neo4j.cypher.execute(query)
	graph_json = scholarly.compute_community_cluster(data, "title", algorithm)

	return json.dumps(graph_json)

@app.route("/authors/cluster/<algorithm>/<int:limit>/cluster/<int:clusterId>")
def author_clusters_cluster_info(algorithm, limit, clusterId):
	
	graph_dict = json.loads(author_clusters(algorithm, limit))
        
	authors_in_cluster = []
        for n in graph_dict["nodes"]:
        	if (n["cluster"] == clusterId):
			keepcharacters_url = (' ')
			new_name_url = "".join(c for c in n["title"].encode('utf-8') if c.isalnum() or c in keepcharacters_url).rstrip()
			keepcharacters_title = (' ', '.', '~', '_')
                        new_name_title = "".join(c for c in n["title"].encode('utf-8') if c.isalnum() or c in keepcharacters_title).rstrip()
                        authors_in_cluster.append({"title" : new_name_title,
                        "url" : "http://dblp.uni-trier.de/search/publ?q=" + urllib.quote(new_name_url)})
        return render_template("cluster_info.html", data=authors_in_cluster);
@app.route("/papers/cluster/<algorithm>/<int:limit>/cluster/<int:clusterId>")
def paper_clusters_cluster_info(algorithm, limit, clusterId):
	query = "MATCH (p1:Paper)-[r:References]->(p2:Paper) RETURN p1.title, p2.title LIMIT %d" % (limit)
	
	data = neo4j.cypher.execute(query)
	graph_dict = scholarly.compute_community_cluster(data, "title", algorithm)

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
			print paper.year
			query_data.append( { "name" : paper.title, "size" : paper.num, "year": paper.year} )
		return json.dumps({"children": query_data})

	elif (category == "author"):
		query = "MATCH (author:Author)-[r:Wrote]->(paper:Paper) RETURN author.name as name, count(r) as num ORDER BY count(r) DESC LIMIT %d" % (limit)
		data = neo4j.cypher.execute(query)
		for author in data:
			query_data.append( { "name" : author.name, "size" : author.num } )
		return json.dumps({"children": query_data})

	elif (category == "institute"):
		query = "MATCH (p:Paper)<-[w:Wrote]-(author:Author)-[r:Affiliated]->(institute:Institute) RETURN institute.` name` as name, count(w) as num ORDER BY count(w) DESC LIMIT %d" % (limit)
		data = neo4j.cypher.execute(query)
		for institute in data:
			query_data.append( { "name" : institute.name, "size" : institute.num } )
		return json.dumps({"children": query_data})
	elif (category == "keyword"):
		keyword_appearances_json = open("static/keyword_appearance.json", "r")
		kw = json.loads(keyword_appearances_json.read())
		result = list()
		for k in kw[:limit]:
			result.append(k)
		return json.dumps(result)
 
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8888)

