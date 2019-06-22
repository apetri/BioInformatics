#!/usr/bin/env python

import sys,os,argparse
import glob
import logging

import pandas as pd

#Parse one file and compute stats
def parseFile(fname):
	
	with open(fname,"r") as fp:
			
		values = []

		#Process one line at a time
		ln = 0
		while True:
			line = fp.readline().strip("\n")
			if not line:
				break

			ch,x1,x2,val = line.split("\t")
			for i in range(int(x1),int(x2)):
				values.append(float(val))

			if not ln%10000:
				logging.debug("Got to chromosome: {0}, overall line: {1} ".format(ch,ln))
			ln = ln + 1

		#Parse array in a DataFrame
		logging.info("Putting values in DataFrame.")
		values = pd.DataFrame({os.path.basename(fname):values})
		
		#Compute stats
		logging.info("Computing stats.")
		stats = values.describe().T
		stats["count"] = stats["count"].astype(int)
		stats.index.name = "filename"

		return stats

#Main
def main():
	
	parser = argparse.ArgumentParser()
	parser.add_argument("filename",help="glob for galaxy file names")
	parser.add_argument("-v","--verbose",action="store_true",default=False,help="display log messages")

	cmd_args = parser.parse_args()

	if cmd_args.filename is None:
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

	#Process one file at a time
	results = []

	for fname in fnames:
		logging.info("Processing file: "+fname)
		results.append(parseFile(fname))

	#Concat all results
	results = pd.concat(results)

	#Output
	results.reset_index().to_html(sys.stdout,index=False)


if __name__=="__main__":
	main()