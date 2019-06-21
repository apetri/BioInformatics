#!/usr/bin/env python

import sys,argparse

#Print in color
def red(s):
	return '\033[31m' + s + '\033[39m'

def green(s):
	return '\033[32m' + s + '\033[39m'

def yellow(s):
	return '\033[33m' + s + '\033[39m'

#Main
def main():
	
	parser = argparse.ArgumentParser()
	parser.add_argument("filename",help="fasta file name")
	parser.add_argument("-p","--pattern",help="pattern to filter")

	cmd_args = parser.parse_args()

	if cmd_args.pattern is None:
		parser.print_help()
		sys.exit(1)

	p1,p2 = cmd_args.pattern.split(",")
	print("[+] Looking for patterns: "+",".join([p1,p2]))

	print("[+] Reading input file: "+cmd_args.filename)
	with open(cmd_args.filename,"r") as fp:
		lines = fp.readlines()

	#Output files
	filename_yes = cmd_args.filename.replace(".fasta","_with_"+"-".join([p1,p2])+".fasta")
	print("[+] Positive matches will be written to: "+filename_yes)

	filename_no = cmd_args.filename.replace(".fasta","_without_"+"-".join([p1,p2])+".fasta")
	print("[+] Negative matches will be written to: "+filename_no)

	#Start search loop
	y = 0
	n = 0

	with open(filename_yes,"w") as fy:
		with open(filename_no,"w") as fn:
			while True:

				pattern_found = False
				buf = list()

				#Read first line of record
				try:
					l = lines.pop(0)
					buf.append(l)
				except IndexError:
					break

				#Read next 4 lines
				for i in range(4):
					l = lines.pop(0)
					buf.append(l)
					if (p1 in l.upper()) or (p2 in l.upper()):
						pattern_found = True

				#Read final \n
				try:
					l = lines.pop(0)
					buf.append(l)
				except IndexError:
					pass

				#See if pattern is found
				if pattern_found:
					print(green("[+] Found pattern: "+p1+"-"+p2))
					y = y+1
					for b in buf:
						fy.write(b)
				else:
					print(red("[-] Pattern not found: "+p1+"-"+p2))
					n = n+1
					for b in buf:
						fn.write(b)

	#Done
	print(green("[+] "+str(y)+" rows have patterns: "+",".join([p1,p2])))
	print(red("[-] "+str(n)+" rows do not have patterns: "+",".join([p1,p2])))
	print("[+] Done.")



if __name__=="__main__":
	main()