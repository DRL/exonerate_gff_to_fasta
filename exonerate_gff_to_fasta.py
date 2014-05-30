#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re, operator, subprocess

class exonerate_gff(object):
	def __init__(self, filename):
		self.filename = filename
		self.data = {}
		self.parameters = ''

def parse_gff_to_dict(filename):
	gff_dict = {}
	query_file, query_id, target_file, target_id, hit, gff_string, gff_flag, dna_flag, dna_string, dna_header = '','','','',0,'', 0, 0, '', ''
	with open(filename) as fh:
		for line in fh:
			if line.startswith("Command line:"):
				cmd_re = re.compile(r".+\[(.+)\]")
				exonerate_cmd = re.match(cmd_re, line).group(1)
				qt_re = re.compile(r"-q\s(\S+).+-t\s(\S+)")
				query_file, target_file = re.search(qt_re, exonerate_cmd).group(1,2)
				gff_dict[query_file+'_'+target_file]={}
				gff_dict[query_file+'_'+target_file]['query_file'] = query_file
				gff_dict[query_file+'_'+target_file]['target_file'] = target_file
				gff_dict[query_file+'_'+target_file]['hit'] = 0
				gff_dict[query_file+'_'+target_file]['dna'] = ''
				gff_dict[query_file+'_'+target_file]['dna_header'] = ''
				gff_dict[query_file+'_'+target_file]['gff'] = ''
			if line.startswith("-- completed exonerate analysis"):
				dna_flag = 0
				gff_dict[query_file+'_'+target_file]['dna'] += dna_string
				gff_dict[query_file+'_'+target_file]['dna_header'] += dna_header
				gff_dict[query_file+'_'+target_file]['gff'] += gff_string
				query_file, query_id, target_file, target_id, hit, gff_string, gff_flag, dna_flag, dna_string, dna_header = '','','','',0,'', 0, 0, '', ''
			if line.startswith("vulgar:"):
				query_id, target_id = operator.itemgetter(1,5)(line.split(" "))
				gff_dict[query_file+'_'+target_file]['query_id'] = query_id
				gff_dict[query_file+'_'+target_file]['target_id'] = target_id
				gff_dict[query_file+'_'+target_file]['hit'] = 1 
			if line.startswith(">"):
				dna_header = line
				dna_flag = 1
			if dna_flag == 1 and not line.startswith(">"):
				dna_string += line.rstrip("\n")
			if line.strip() == '':
				dna_flag = 0
			if gff_flag == 1 :
				gff_string += line
			if line.startswith("##gff-version 2"):
				gff_flag = 1
				gff_string += line
			if line.startswith("# --- END OF GFF DUMP ---"):
				gff_flag = 0
	return gff_dict

def export_files(gff_dict):
	for record in gff_dict:
		if gff_dict[record]['hit'] == 1: 
			base_file = gff_dict[record]['target_id']
			
			gff_file = base_file + '.gff'
			gff_fh = open(gff_file, 'w')
			gff_string = gff_dict[record]['gff']
			gff_fh.write(gff_string)	
			gff_fh.close()

			dna_file = base_file + '.cds.fa'
			cds_header = gff_dict[record]['dna_header']
			cds = gff_dict[record]['dna']
			cds_fh = open(dna_file, 'w')
			cds_fh.write(">" + cds_header + cds)
			cds_fh.close()
			
			aa_file = base_file + '.aa.fa'
			aa = subprocess.call("/exports/software/emboss/EMBOSS-6.6.0/emboss/transeq " + dna_file + " " + aa_file , shell=True)



if __name__ == "__main__":
	gff_file = sys.argv[1]
	gff_dict = parse_gff_to_dict(gff_file)
	export_files(gff_dict)