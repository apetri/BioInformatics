"""
Find bp summits which are within a fixed distance from mart regions

"""
from __future__ import division

import sys
import ConfigParser

import numpy as np
import pandas as pd

#####################
#PeakMartCross class#
#####################

class PeakMartCross(object):

	"""
	Class handler for mart/peaks cross analysis

	"""

	#Constructor
	def __init__(self,peaks,mart):
		self._peaks = peaks
		self._mart = mart

	#Getters
	@property
	def peaks(self):
		return self._peaks

	@property
	def mart(self):
		return self._mart

	#Build from files
	@classmethod
	def from_files(cls,peak_fname,mart_fname,peak_kwargs={},mart_kwargs={}):

		#Read files
		peaks = cls.read_peaks(peak_fname,**peak_kwargs)
		mart = cls.read_mart(mart_fname,**mart_kwargs)

		#Build and return
		return cls(peaks,mart)

	#Readers
	@staticmethod
	def read_mart(fname):

		#Read and format
		mart = pd.read_excel(fname,names=("project","chromosome","gstart","gend"))
		
		#Assign ID to mart region
		mart["gid"] = mart.groupby("chromosome")["gstart"].transform(lambda s:np.arange(len(s)))

		#Return
		return mart

	@staticmethod
	def read_peaks(fname):

		#Read and format
		pk = pd.read_csv(fname,header=None,names=("chromosome","pstart","pend"),sep="\t")
		pk["chromosome"] = pk["chromosome"].str.strip("chr")
		pk["pmid"] = pk.eval("(pstart+pend)/2").astype(int)
		pk["pampl"] = pk.eval("pend-pstart")

		#Assign ID to mart region
		pk["pid"] = pk.groupby("chromosome")["pstart"].transform(lambda s:np.arange(len(s)))

		#Return
		return pk

	#Change peak amplitude interval
	def setPampl(self,pampl):

		self._peaks["pampl"] = pampl
		self._peaks["pstart"] = self._peaks["pmid"] - pampl//2 
		self._peaks["pend"] = self._peaks["pmid"] + pampl//2

	#######################################
	#######Mart region finder##############
	#######################################

	#Operate by chromosome
	@staticmethod
	def pkfind_chromosome(peaks,mart,bp_tolerance=2000):

		#Start, end of bp peaks
		ps,pe = peaks.pstart.values,peaks.pend.values

		#Start,end of mart regions
		gs,ge = mart.gstart.values,mart.gend.values

		#Distance array
		distances = np.empty((4,len(ps),len(gs)),dtype=np.int)
		distances[0] = np.abs(ps[:,None] - gs[None])
		distances[1] = np.abs(ps[:,None] - ge[None])
		distances[2] = np.abs(pe[:,None] - gs[None])
		distances[3] = np.abs(pe[:,None] - ge[None])

		#Compute minimum distance between extremes
		distances = distances.min(0)
		pid,gid = np.where(distances<=bp_tolerance)

		#Construct DataFrame with ids, distances
		cross_df = pd.DataFrame({"pid":pid,"gid":gid})
		cross_df["distance"] = distances[pid,gid]

		#Merge gene extremes by pid, gid
		cross_df = pd.merge(cross_df,peaks[["pstart","pend","pampl","pid"]],on="pid",how="left")
		cross_df = pd.merge(cross_df,mart[["project","gstart","gend","gid"]],on="gid",how="left")

		#Return
		return cross_df

	#Merge results across chromosomes
	def pkfind(self,bp_tolerance=2000):

		#Group by chromosome
		pk_grp = self.peaks.groupby("chromosome")
		mart_grp = self.mart.groupby("chromosome")

		#List of results, by chromosome
		cross_all = list()

		#Cycle over chromosomes
		for ch in pk_grp.groups:
			cross_df = self.pkfind_chromosome(pk_grp.get_group(ch),mart_grp.get_group(ch),bp_tolerance=bp_tolerance)
			cross_df["chromosome"] = ch
			cross_all.append(cross_df)

		#Concatenate, reorder, return
		column_order = ["project","chromosome","pstart","pend","pampl","gstart","gend","distance","gid","pid"]
		cross_all = pd.concat(cross_all,axis=0,ignore_index=True)
		return cross_all[column_order]

###########################
#########Execution#########
###########################

def main():
	
	#Check number of arguments
	if len(sys.argv)<2:
		print("Usage: python {0} config_file.ini".format(sys.argv[0]))
		sys.exit(1)

	#Read configuration
	options = ConfigParser.ConfigParser()
	print("[+] Reading options from: {0}".format(sys.argv[1]))
	options.read(sys.argv[1])
	section = "PeakMart"

	#Read in datasets
	peak_file = options.get(section,"peak_file")
	print("[+] Reading bp peaks from: {0}".format(peak_file))
	mart_file = options.get(section,"mart_file")
	print("[+] Reading mart regions from: {0}".format(mart_file))

	data = PeakMartCross.from_files(peak_file,mart_file)

	#Set bp interval
	pampl = options.getint(section,"pampl")
	print("[+] Setting bp interval to: {0}".format(pampl))
	data.setPampl(pampl)

	#Find cross regions
	bp_tolerance = options.getint(section,"bp_tolerance")
	print("[+] Finding cross regions in data, with tolerance: {0} bp".format(bp_tolerance))
	cross = data.pkfind(bp_tolerance=bp_tolerance)

	#Output
	outfile = options.get(section,"output_file")
	print("Writing result to: {0}".format(outfile))
	cross.to_excel(outfile)

if __name__=="__main__":
	main()


