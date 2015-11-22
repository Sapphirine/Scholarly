* Dataset Preparation:
** Import into Neo4j:
*** Use import-csv tool. You can refer to the script for more detailed information.

neo4j-import --into mag.db --nodes:Author "Authors-header.txt,Authors.txt" --nodes:ConferenceSeries "ConferenceSeries-header.txt,ConferenceSeries.txt" --nodes:FieldOfStudy "FieldsOfStudy-header.txt,FieldsOfStudy.txt" --nodes:Paper "Papers-header.txt,Papers.zip" --relationships:References "Paper-References-header.txt,PaperReferences.zip” --relationships:Written “Paper-Author-header.txt,PaperAuthorAffiliations.zip” --relationships:field “Paper-Field-header.txt,PaperKeywords.zip" --skip-bad-relationships true --delimeter "\t" --ignore-extra-columns true
