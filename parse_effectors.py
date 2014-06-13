#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, collections

def parse_fasta_to_dict(fasta_file):
	protein_dict = collections.defaultdict(dict) 
	with open(fasta_file) as fh:
		header = ''
		seq = ''
		for line in fh:
			line = line.rstrip("\n").rstrip("\r")
			if line.startswith(">"):
				if (header):
					print seq
					protein_dict[header]['seq'] = seq
					if (seq.startswith("M")):
						protein_dict[header]['has_start'] = 1
					else:
						protein_dict[header]['has_start'] = 0
					if "X" in seq:
						protein_dict[header]['has_X'] = 1
					else:
						protein_dict[header]['has_X'] = 0
					if "*" in seq:
						protein_dict[header]['has_stop'] = 1
						protein_dict[header]['length_before_stop'] = len(seq[0:seq.index('*')])
					else:
						protein_dict[header]['has_stop'] = 0
						protein_dict[header]['length_before_stop'] = len(seq)

				seq = ''
				header = line.split(' ')[0][1:]
			else:
				seq += line
		protein_dict[header]['seq'] = seq
		if (seq.startswith("M")):
			protein_dict[header]['has_start'] = 1
		else:
			protein_dict[header]['has_start'] = 0
		if "X" in seq:
			protein_dict[header]['has_X'] = 1
		else:
			protein_dict[header]['has_X'] = 0
		if "*" in seq:
			protein_dict[header]['has_stop'] = 1
			protein_dict[header]['length_before_stop'] = len(seq[0:seq.index('*')])
		else:
			protein_dict[header]['has_stop'] = 0
			protein_dict[header]['length_before_stop'] = len(seq)
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
	#blast_file = protein_file + ".no_cellulases.out"
	
	protein_dict = parse_fasta_to_dict(protein_file)
	print protein_dict
	#blast_dict = parse_blast_to_dict(blast_file)
	print 'protein' + "\t" + 'reference' + "\t" + 'has_start' + "\t" + 'has_stop' + "\t" + 'length_before_stop' + "\t" + 'has_X' 
	for protein in sorted(protein_dict):
		if protein_dict[protein]['has_start'] == 1 and protein_dict[protein]['has_X'] == 0:
			print protein + "\t" + str(protein_dict[protein]['has_start']) + "\t" + str(protein_dict[protein]['has_stop']) + "\t" + str(protein_dict[protein]['length_before_stop']) + "\t" + str(protein_dict[protein]['has_X']) 
		else:
			pass