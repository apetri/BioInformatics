#!/usr/bin/env python

import sys,os,argparse
import glob
import logging

import pandas as pd
from bs4 import BeautifulSoup

#Parse HTML stats
def parseHTML(fname):
	
	with open(fname,"r") as fp:
		soup = BeautifulSoup(fp.read(),"html.parser")

	#Rows
	columns = list()
	for col in soup.thead.tr.find_all("th"):
		columns.append(col.text)

	#Header
	rows = list()
	for row in soup.tbody.find_all("tr"):
		vals = list()
		for n,val in enumerate(row.find_all("td")):
			if not n:
				vals.append(val.text)
			else:
				vals.append(float(val.text))

		rows.append(vals)

	return pd.DataFrame.from_records(rows,columns=columns).set_index("filename")

#Main
def main():
	
	parser = argparse.ArgumentParser()
	parser.add_argument("filename",help="glob for galaxy file names")
	parser.add_argument("--stats",help="HTML file with computed stats")
	parser.add_argument("--outdir",help="output directory")
	parser.add_argument("-v","--verbose",action="store_true",default=False,help="display log messages")

	cmd_args = parser.parse_args()

	if (cmd_args.filename is None) or (cmd_args.stats is None) or (cmd_args.outdir is None):
		parser.print_help()
		sys.exit(1)

	#Log level
	if cmd_args.verbose:
		logging.basicConfig(level=logging.DEBUG)
	else:
		logging.basicConfig(level=logging.INFO)

	#Find file names to process
	fnames = glob.glob(cmd_args.filename)
	logging.info("Pattern: {0} --> found {1} files to process.".format(cmd_args.filename,len(fnames)))

	#Check if output directory exists
	if not os.path.exists(cmd_args.outdir):
		logging.info("Creating output directory: "+cmd_args.outdir)
		os.mkdir(cmd_args.outdir)
	logging.info("Saving outputs to: "+cmd_args.outdir)

	#Load stats
	logging.info("Loading pre-computed stats from: "+cmd_args.stats)
	stats = parseHTML(cmd_args.stats)

	#Process one file at a time
	for fname in fnames:
		logging.info("Processing file: "+fname)

		#Stats are indexed by basename
		fbase = os.path.basename(fname)
		norm = stats["50%"][fbase]

		#Output written to this file
		outfname = os.path.join(cmd_args.outdir,fbase)
		logging.info("Normalized output will be written to: "+outfname)

		#Open both files and cycle over rows
		with open(fname,"r") as fin:
			with open(outfname,"w") as fout:

				while True:
					
					line = fin.readline().strip("\n")
					if not line:
						break

					#Normalize
					parsed = line.split("\t")
					parsed[-1] = "{0:.4f}".format(float(parsed[-1])/norm)

					#Write output row
					fout.write("\t".join(parsed)+"\n")

if __name__=="__main__":
	main()