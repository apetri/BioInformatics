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

				#Allocate space for field
				if field not in meta:
					meta[field] = dict()

				#Split subfields
				value = value.strip("<").strip(">")
				for spec in value.split(","):

					#TODO: temporary
					try:
						subfield,subvalue = spec.split("=")
					except:
						continue

					#Allocate space for subfield
					if subfield not in meta[field]:
						meta[field][subfield] = list()

					#Fill in value
					meta[field][subfield].append(subvalue)

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

		#Reformat metadata in a convenient way
		for field in ["INFO","FILTER","FORMAT"]:
			if field in meta:
				meta[field] = pd.DataFrame.from_dict(meta[field]).set_index("ID")

		#Instantiate and return
		return cls(data,meta)



