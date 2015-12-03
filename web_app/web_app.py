import py2neo
import json
import flask
from py2neo import Graph, authenticate

app = flask.Flask(__name__)


authenticate("localhost:7474","neo4j", "BigData1")
graph = Graph()
@app.route("/")
def hello():
	return "Hello World!"

@app.route("/test")
def get_test():
    return flask.render_template("index.html")

@app.route("/test2")
def get_graph():
	#Execute query to get data
	query = "MATCH (p1:Paper)-[r:References]->(p2:Paper) RETURN p1.title as p1, p2.title as p2 LIMIT 25"
	data = graph.cypher.execute(query)
	
	return json.dumps([{"paper": row.p1} for row in data])

if __name__ == "__main__":
	app.run(host='104.131.209.152')
	flask.url_for('static', filename='test.json')
