import unicodecsv as csv
import sys
dblp_file = open(sys.argv[1], "r")
dblp_papers = open("dblp_papers.csv", "w")
dblp_author = open("dblp_author.csv", "w")
dblp_ref = open("dblp_ref.csv", "w")
dblp_auth_paper = open("dblp_auth_paper.csv", "w")

paper_wr = csv.writer(dblp_papers)
author_wr = csv.writer(dblp_author)
ref_wr = csv.writer(dblp_ref)
auth_paper_wr = csv.writer(dblp_auth_paper)

papers_line = []
authors = None
ref_line = []

AUTHOR_ID = 0

INDEX = ""

for rline in dblp_file:
	line = rline.decode("utf-8").rstrip()

	if line.startswith("#index"):
		INDEX = line.lstrip("#index")
		papers_line.append(INDEX)
	if line.startswith("#*"):
		papers_line.append(line.lstrip("#*").replace("\"",'_'))
	if line.startswith("#c"):
		papers_line.append(line.lstrip("#c"))
	if line.startswith("#t"):
		papers_line.append(line.lstrip("#t"))
	if line.startswith("#@"):
		authors = line.lstrip("#@").split(",")
	if line.startswith("#%"):
		ref = line.lstrip("#%")
		ref_line.append(ref)
	if line.startswith("#!"):
		abstract = line.lstrip("#!").replace("\n"," ")
		papers_line.append(abstract)
	if line == "":
		#print papers_line
		paper_wr.writerow(papers_line)
		
		for a in authors:
			author_wr.writerow([AUTHOR_ID, a])
			auth_paper_wr.writerow([INDEX, AUTHOR_ID])
			AUTHOR_ID += 1

		for r in ref_line:
			if (r != ""):
				ref_wr.writerow([INDEX, r])

		papers_line = []
		authors = None
		ref_line = []

dblp_file.close()
dblp_papers.close()
dblp_author.close()
dblp_ref.close()
dblp_auth_paper.close()

