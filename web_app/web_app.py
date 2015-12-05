import json
import flask
from py2neo import Graph, authenticate
from py2neo.packages.httpstream import http

http.socket_timeout = 9999

app = flask.Flask(__name__)


authenticate("localhost:7474","neo4j", "BigData1")
neo4j = Graph()
@app.route("/")
def get_index():
    return flask.render_template("index.html")

@app.route("/test")
def get_test():
    return flask.render_template("bar_chart.html")

#Data preparation
@app.route("/institutes_published_most")
def get_institutes_published_most():
	query = "MATCH (p:Paper)<-[w:Wrote]-(author:Author)-[r:Affiliated]->(institute:Institute) RETURN institute.` name` as name, count(w) as num ORDER BY count(w) DESC LIMIT 25"
	data = neo4j.cypher.execute(query)
	bardata = []
	for institute in data:
		bardata.append( { "InstituteName" : institute.name, "PublishNum" : institute.num } )
	return json.dumps(bardata)

@app.route("/top_authors_within_top_institutes")
def get_top_authors_within_top_institutes():
	query = "MATCH (p:Paper)<-[:Wrote]-(a:Author)-[:Affiliated]->(i:Institute) WHERE i.instituteId=\"601057\" RETURN a.name as name, count(p.title) as num ORDER BY count(p.title) DESC"
	data = neo4j.cypher.execute(query)
	bardata = []
	for author in data:
		bardata.append( { "AuthorName" : author.name, "PublishNum" : author.num } )
	return json.dumps(bardata)

@app.route("/top_authors")
def get_top_authors():
	query = "MATCH (author:Author)-[r:Wrote]->(paper:Paper) RETURN author.keyterms as keyterms, author.name as name, count(r) as num ORDER BY count(r) DESC LIMIT 25"
	data = neo4j.cypher.execute(query)
	bubbledata = []
	for author in data:
		bubbledata.append( { "AuthorName" : author.name, "Keyterms" : author.keyterms, "PublishNum" : author.num } )
	return json.dumps(bubbledata)

@app.route("/top_reference")
def get_top_reference():
	query = "MATCH (paper1:Paper)-[r:References]->(paper2:Paper) RETURN paper2.title as title, paper2.abstract as abstract, paper2.year as year, paper2.venue as venue, count(r) as num ORDER BY count(r) DESC LIMIT 25"
	data = neo4j.cypher.execute(query)
	bubbledata = []
	for paper in data:
		bubbledata.append( { "Title" : paper.title, "Venue" : paper.venue, "Year" : paper.year, "Abstract" : paper.abstract, "RefNum" : paper.num } )
	return json.dumps(bubbledata)


if __name__ == "__main__":
	app.run(host='104.131.209.152')
#	flask.url_for('static', filename='test.json')
