import unicodecsv as csv
import re
import sys
import pandas as pd
from sets import Set

def parsePapersToCSV(papers_file):
	dblp_papers = open("dblp_papers.csv", "w")
	dblp_ref = open("dblp_ref.csv", "w")

	paper_wr = csv.writer(dblp_papers, quoting=csv.QUOTE_ALL)
	ref_wr = csv.writer(dblp_ref)

	INDEX = ""
	row = []
	ref_line = []
	for rline in papers_file:
		line = rline.decode("utf-8").rstrip().replace("\n","").replace("\"", "").replace('\\', "")
		if line.startswith("#index"):
			INDEX = line.lstrip("#index")
			row.append(INDEX)
		if line.startswith("#*"):
			row.append(line.lstrip("#*"))
		if line.startswith("#c"):
			row.append(line.lstrip("#c"))
		if line.startswith("#t"):
			row.append(line.lstrip("#t"))
		if line.startswith("#%"):
			ref = line.lstrip("#%")
			ref_line.append(ref)
		if line.startswith("#!"):
			abstract = line.lstrip("#!")
			if (abstract == ""):
				abstract = ""
			row.append(abstract)
		if line == "":
			paper_wr.writerow(row)
			
			for r in ref_line:
				if (r != ""):
					ref_wr.writerow([INDEX, r])

			row = []
			ref_line = []

	dblp_papers.close()
	dblp_ref.close()

def parseAuthorToCSV(author_file):
	
	dblp_authors = open("dblp_author.csv","w")

	author_wr = csv.writer(dblp_authors,quoting=csv.QUOTE_ALL)

	row = []

	for rline in author_file:
		line = rline.decode("utf-8").rstrip().replace("\n","")

		if line.startswith("#index"):
			index= line.lstrip("#index")
			row.append(index)
		if line.startswith("#n"):
			name = line.lstrip("#n")
			row.append(name)
		if line.startswith("#a"):
			continue
		if line.startswith("#t"):
			keyterms = line.lstrip("#t")
			row.append(keyterms)
		if line == "":
			author_wr.writerow(row)
			row = []

	dblp_authors.close()

def parseAffiliationsToCSV(aff_file):

	dblp_aff = open("dblp_aff.csv","w")
	aff_wr = csv.writer(dblp_aff, quoting=csv.QUOTE_ALL)

	aff_set = Set()

	for rline in aff_file:
		line = rline.decode("utf-8").rstrip().replace("\n","")

		if line.startswith("#index"):
			continue
		if line.startswith("#n"):
			continue
		if line.startswith("#a"):
			affs = line.lstrip("#a").split(";")
			for a in affs:
				aff_set.add(a)

		if line.startswith("#t"):
			continue
		if line == "":
			continue

	AFF_INDEX = 0

	for aff in aff_set:
		aff_wr.writerow([AFF_INDEX,aff])
		AFF_INDEX += 1

	dblp_aff.close()

def parseAuthorAffiliationsToCSV(authors_file, aff_file):
	aff_df = csv.reader(open(aff_file, 'r'))
	authors_df = open(authors_file, 'r')
	aff_map = {}

	dblp_aa = open("dblp_author2affiliation.csv", "w")
	aa_wr = csv.writer(dblp_aa)

	for a in aff_df:
		aff_map[a[1]] = a[0]

	INDEX = ""
	for rline in authors_df:
		line = rline.decode("utf-8").rstrip().replace("\n","")

		if line.startswith("#index"):
			INDEX = line.lstrip("#index")
		if line.startswith("#n"):
			continue
		if line.startswith("#a"):
			aff = line.lstrip("#a").split(";")
			for a in aff:
				if (a != ""):
					aa_wr.writerow([INDEX, aff_map[a]])
		if line.startswith("#t"):
			continue
		if line == "":
			continue

	dblp_aa.close()

if __name__ == "__main__":
	papers = open(sys.argv[1], 'r')
	parsePapersToCSV(papers)

	authors = open(sys.argv[2], 'r')
	parseAuthorToCSV(authors)

	authors = open(sys.argv[2], 'r')
	parseAffiliationsToCSV(authors)


	parseAuthorAffiliationsToCSV(sys.argv[2], "dblp_aff.csv")
