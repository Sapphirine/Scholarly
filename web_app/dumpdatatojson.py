import py2neo
import igraph
import json
from py2neo import Graph as pGraph, authenticate
from igraph import Graph as iGraph
from py2neo.packages.httpstream import http

http.socket_timeout = 9999
#Connect to Neo4j
authenticate("localhost:7474","neo4j", "BigData1")
neo4j = pGraph()

#Execute query to get data
# query = "MATCH (p:Paper)<-[w:Wrote]-(author:Author)-[r:Affiliated]->(institute:Institute) RETURN institute.` name` as name, count(w) as num ORDER BY count(w) DESC LIMIT 25"
# data = neo4j.cypher.execute(query)
# name = []
# for institute in data:
# 	name.append( { "InstituteName" : institute.name, "PublishNum" : institute.num } )
# print json.dumps(name)
query = "MATCH (author:Author)-[r:Wrote]->(paper:Paper) RETURN author.name as name, count(r) as num ORDER BY count(r) DESC LIMIT 25"
data = neo4j.cypher.execute(query)
bubbledata = []
for author in data:
	bubbledata.append( { "packageName" : author.name, "className" : author.name, "value" : author.num } )
with open('test.json', 'w') as outfile:
	json.dump({"children":bubbledata}, outfile)