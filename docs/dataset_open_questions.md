* What institutes publish the most?
MATCH (author:Author)-[r:Affiliated]->(institute:Institute) RETURN institute, count(r) ORDER BY count(r) DESC LIMIT 25


* What are the top authors for each Institute?


* Who are the top authors?
MATCH (author:Author)-[r:Wrote]->(paper:Paper) RETURN author, count(r) ORDER BY count(r) DESC LIMIT 25

* Determine what area of CS does each Paper belong to using keyterms.

* What are each authors specializations? (Using keyterms)

* Top papers?
MATCH (paper1:Paper)-[r:References]->(paper2:Paper) RETURN paper2, count(r) ORDER BY count(r) DESC LIMIT 25

* How are the top papers related? (Get top 100 papers. Then find the appropriate paper body and do separate analysis?)

* How long after their first publications do authors reach their "publication" prime? (Publication Trend among authors)

