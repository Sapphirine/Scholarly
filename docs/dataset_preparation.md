* Dataset Preparation:
** Import into Neo4j:
*** Use import-csv tool. You can refer to the script for more detailed information.

neo4j-import --into mag.db --nodes:Author "Authors-header.txt,Authors.txt" --nodes:ConferenceSeries "ConferenceSeries-header.txt,ConferenceSeries.txt" --nodes:FieldOfStudy "FieldsOfStudy-header.txt,FieldsOfStudy.txt" --nodes:Paper "Papers-header.txt,Papers.txt" --relationships:References "Paper-References-header.txt,PaperReferences.txt” --relationships:Written “Paper-Author-header.txt,PaperAuthorAffiliations.txt” --relationships:field “Paper-Field-header.txt,PaperKeywords.txt"

ArnetMiner-DBLP:
https://aminer.org/billboard/citation

neo4j-import --into dblp.db --nodes:Author "dblp_author-header.csv,dblp_author.csv" --nodes:Paper "dblp_papers-header.csv,dblp_papers.csv" --relationships:Wrote "dblp_auth_paper-header.csv,dblp_auth_paper.csv" --relationships:References "dblp_ref-header.csv,dblp_ref.csv" --ignore-empty-columns true --bad-tolerance 10000000

AMiner Dataset:
https://aminer.org/billboard/AMinerNetwork

neo4j-import --into dblp.db --nodes:Author "dblp_author-header.csv,dblp_author.csv" --nodes:Paper "dblp_papers-header.csv,dblp_papers.csv" --nodes:Institute "dblp_aff-header.csv,dblp_aff.csv" --relationships:Wrote "dblp_author2paper-header.csv,dblp_author2paper.csv" --relationships:References "dblp_ref-header.csv,dblp_ref.csv" --relationships:Affiliated "dblp_author2affiliation-header.csv,dblp_author2affiliation.csv" --ignore-empty-strings true --ignore-extra-columns true --bad-tolerance 1000000
