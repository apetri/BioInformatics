#!/usr/bin/env python

#system
import sys
import argparse
import logging

#3rd party
import scipy.io
import biosppy.signals as bs

######
#Main#
######

def main():

	#Log level
	logging.basicConfig(level=logging.INFO)
	
	#Command line arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("-i","--in",dest="input",help="Input .mat file with ECG signals")
	parser.add_argument("-o","--out",dest="output",help="Ouput .mat file with R peak locations")

	#Parse arguments
	cmd_args = parser.parse_args()
	if (cmd_args.input is None) or (cmd_args.output is None):
		parser.print_help()
		sys.exit(1)

	#Read input file
	logging.info("Reading ECG signal from: {0}".format(cmd_args.input))
	signal = scipy.io.loadmat(cmd_args.input)["EKG_epochs"]
	logging.info("Found {0[0]} epochs, with {0[1]} samples each.".format(signal.shape))

	#Extract peaks
	rpeaks = list()
	for n in range(len(signal)):
		logging.info("Processing epoch {0} of {1}...".format(n+1,len(signal)))
		out = bs.ecg.ecg(signal=signal[n],sampling_rate=256.,show=False)
		rpeaks.append(out["rpeaks"])

	#Save peaks
	logging.info("Saving R peak locations to: {0}".format(cmd_args.output))
	scipy.io.savemat(cmd_args.output,{"rpeaks":rpeaks})

#Execute
if __name__=="__main__":
	main()