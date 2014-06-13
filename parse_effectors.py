#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, collections

def parse_fasta_to_dict(fasta_file):
	protein_dict = {}
	with open(fasta_file) as fh:
		header = ''
		seq = ''
		for line in fh:
			line = line.rstrip("\n")
			if line.startswith(">"):
				if (header):
					protein_dict[header] = seq
				seq = ''
				header = line.split(' ')[0][1:]
			else:
				seq += line
		protein_dict[header] = seq
	return protein_dict

def parse_blast_to_dict(blast_file):
	blast_dict = collections.defaultdict(dict) 
	with open(blast_file) as fh:
		for line in fh:
			temp = line.rstrip("\n").rsplit("\t")
			query, subject, evalue = str(temp[0]), str(temp[1]), float(temp[10])
			if query in blast_dict:
				if subject in blast_dict[query]:
					if evalue >= blast_dict[query][subject]:
						continue
					else:
						blast_dict[query][subject] = evalue
				else:
					blast_dict[query][subject] = evalue
			else:
				blast_dict[query][subject] = evalue
	return blast_dict

if __name__ == "__main__":
	protein_file = sys.argv[1]
	blast_file = sys.argv[2]
	
	protein_dict = parse_fasta_to_dict(protein_file)
	blast_dict = parse_blast_to_dict(blast_file)

	print protein_dict
	