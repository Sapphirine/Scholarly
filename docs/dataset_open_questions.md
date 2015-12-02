* What institutes publish the most?
MATCH (p:Paper)<-[w:Wrote]-(author:Author)-[r:Affiliated]->(institute:Institute) RETURN institute, count(w) ORDER BY count(w) DESC LIMIT 25

* What are the top authors within top institutes?
MATCH (p:Paper)<-[:Wrote]-(a:Author)-[:Affiliated]->(i:Institute) WHERE i.instituteId="601057" RETURN a.name, count(p.title) ORDER BY count(p.title) DESC


* Who are the top authors?
MATCH (author:Author)-[r:Wrote]->(paper:Paper) RETURN author, count(r) ORDER BY count(r) DESC LIMIT 25

* Determine what area of CS does each Paper belong to using keyterms.

* What are each authors specializations? (Using keyterms)

* Top referenced papers?
MATCH (paper1:Paper)-[r:References]->(paper2:Paper) RETURN paper2, count(r) ORDER BY count(r) DESC LIMIT 25

* Authors with top referenced papers?
MATCH (paper1:Paper)-[r:References]->(paper2:Paper)<-[r2:Wrote]-(a:Author) RETURN a, count(r) ORDER BY count(r) DESC LIMIT 25

* How are the top papers related? (Get top 100 papers. Then find the appropriate paper body and do separate analysis?)

* How long after their first publications do authors reach their "publication" prime? (Publication Trend among authors)

* What is the rate at which top authors publish?

* H-Index for top authors?

* Top Collaborators for each author? (Which authors collaborate more outside of their own institute?)

* Is there a relationship between Venue & # of citations? (Are papers from top conferences cited more due to exposure?)

* How has the number of publications over the years changed?
