"""
Lightweight I/O for VCF files 

"""

import re
import pandas as pd

###############
#VCFData class#
###############

class VCFData(object):

	#Constructor
	def __init__(self,data,meta):
		self._data = data
		self._meta = meta

	#Getters
	@property
	def data(self):
		return self._data

	@property
	def meta(self):
		return self._meta

	@property
	def columns(self):
		return self.meta["columns"] 

	##############
	#Input/output#
	##############

	#Read metadata
	@staticmethod
	def _read_meta(fp):
		meta = dict()

		#Read each line of metadata until the column names are found
		while True:
			line = fp.readline().strip("\n")

			#If we found the column header, we are done
			if line.startswith("#CHROM"):
				meta["columns"] = filter(lambda n:n,line[1:].split(" "))
				return meta

			#Strip the first ##
			line = line.strip("##")
			field,value = re.match(r"(.*?)=(.*)",line).groups()

			#Separate cases for INFO, FILTER, FORMAT
			if field in ["INFO","FILTER","FORMAT"]:
				#TODO: temporary
				meta[field] = value
			else:
				meta[field] = value

	#Read data
	@staticmethod
	def _read_data(fp,columns):
		return pd.read_csv(fp,delim_whitespace=True,header=None,names=columns,na_values=".")

	#Read single file
	@classmethod
	def read(cls,fname):

		#Read the file
		with open(fname,"r") as fp:
			meta = cls._read_meta(fp)
			columns = meta["columns"]
			data = cls._read_data(fp,columns)

		#Instantiate and return
		return cls(data,meta)



