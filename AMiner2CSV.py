"""Usage:
   AMiner2CSV.py paper_file author_file author2paper_file

"""
import unicodecsv as csv
import time
from sets import Set
from tqdm import *
from docopt import docopt

PAPERS_OUT = "dblp_papers.csv"
REF_OUT = "dblp_ref.csv"
AUTHOR_OUT = "dblp_author.csv"
AFF_OUT = "dblp_aff.csv"
A2A_OUT = "dblp_author2aff.csv"
A2P_OUT = "dblp_author2paper.csv"

def parsePapersToCSV(papers_filename):
	
	global PAPERS_OUT
	global REF_OUT

	papers_file = open(papers_filename, 'r')

	dblp_papers = open(PAPERS_OUT, "w")
	dblp_ref = open(REF_OUT, "w")

	paper_wr = csv.writer(dblp_papers, quoting=csv.QUOTE_ALL)
	ref_wr = csv.writer(dblp_ref)

	INDEX = ""
	row = []
	ref_line = []
	for rline in tqdm(papers_file):
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
	papers_file.close()

def parseAuthorToCSV(author_filename):
	
	global AUTHOR_OUT

	author_file = open(author_filename, 'r')
	dblp_authors = open(AUTHOR_OUT,"w")

	author_wr = csv.writer(dblp_authors,quoting=csv.QUOTE_ALL)

	row = []

	for rline in tqdm(author_file):
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
	author_file.close()

def parseAffiliationsToCSV(aff_filename):

	global AFF_OUT

	aff_file = open(aff_filename, 'r')
	dblp_aff = open(AFF_OUT,"w")
	aff_wr = csv.writer(dblp_aff, quoting=csv.QUOTE_ALL)

	aff_set = Set()

	for rline in tqdm(aff_file):
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

	for aff in tqdm(aff_set):
		aff_wr.writerow([AFF_INDEX,aff])
		AFF_INDEX += 1

	dblp_aff.close()
	aff_file.close()

def parseAuthorAffiliationsToCSV(authors_filename, aff_filename):
	
	global A2A_OUT

	aff_file = open(aff_filename, 'r')
	authors_file = open(authors_filename, 'r')

	aff_df = csv.reader(aff_file)
	aff_map = {}

	dblp_aa = open(A2A_OUT, "w")
	aa_wr = csv.writer(dblp_aa)

	for a in aff_df:
		aff_map[a[1]] = a[0]

	INDEX = ""
	for rline in tqdm(authors_file):
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
	aff_file.close()
	authors_file.close()

def parseAuthor2PaperToCSV(author2paper_filename):
	
	global A2P_OUT

	a2p_file = open(author2paper_filename, 'r')
	a2p_out = open(A2A_OUT, "w")

	for line in tqdm(a2p_file):
		a2p_out.write(line.replace("\t",','))

	a2p_file.close()
	a2p_out.close()
	

if __name__ == "__main__":
	args = docopt(__doc__)

	papers_file = args['paper_file']
	author_file = args['author_file']
	a2p_file = args['author2paper_file']

	print "Papers2CSV"
	parsePapersToCSV(papers_file)
	print "Author2CSV"
	parseAuthorToCSV(author_file)
	print "Aff2CSV"
	parseAffiliationsToCSV(author_file)
	print "Author2AffCSV"
	parseAuthorAffiliationsToCSV(author_file, AFF_OUT)
	print "Author2PaperCSV"
	parseAuthor2PaperToCSV(a2p_file)
