#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re, operator

class exonerate_gff(object):
	def __init__(self, filename):
		self.filename = filename
		self.data = {}
		self.parameters = ''

def parse_gff_to_dict(filename):
	gff_dict = {}
	query_file, query_id, target_file, target_id, hit, gff_string, gff_flag = '','','','',0,'', 0
	with open(filename) as fh:
		for line in fh:
			if line.startswith("Command line:"):
				query_file, query_id, target_file, target_id, hit, gff_string, gff_flag = '','','','',0,'', 0
				cmd_re = re.compile(r".+\[(.+)\]")
				exonerate_cmd = re.match(cmd_re, line).group(1)
				qt_re = re.compile(r"-q\s(\S+).+-t\s(\S+)")
				query_file, target_file = re.search(qt_re, exonerate_cmd).group(1,2)
				gff_dict[query_file+'_'+target_file]={}
				gff_dict[query_file+'_'+target_file]['hit']=0
			elif line.startswith("Hostname"):
				continue
			elif line.startswith("vulgar:"):
				#query_id, target_id = operator.itemgetter(1,5)(line.split(" "))
				query_id, target_id = operator.itemgetter(1,5)(line.split(" "))
				gff_dict[query_file+'_'+target_file]['query_id'], gff_dict[query_file+'_'+target_file]['target_id'] = query_id, target_id
				#hit = 1
				gff_dict[query_file+'_'+target_file]['hit']=1
			elif line.startswith("##gff-version 2"):
				gff_flag = 1
				gff_string += line
			elif line.startswith("# --- END OF GFF DUMP ---"):
				gff_flag = 0
			elif gff_flag == 1:
				gff_string += line
				if line.startswith(target_id):
					columns = line.split('\s{2,}')
			elif line.startswith("-- completed exonerate analysis"):
				#print query_file, target_file, hit
				#print query_id, target_id
				gff_dict[query_file+'_'+target_file]['gff'] = gff_string
			else:
				continue
	return gff_dict

def export_files(gff_dict):
	for record in gff_dict:
		if gff_dict[record]['hit'] == 1:
			
			base_file = gff_dict[record]['target_id']
			gff_file = base_file + '.gff'
			exon_file = base_file + '.exons.fa'
			cdna_file = base_file + '.cdna.fa'
			aa_file = base_file + '.aa.fa'
			gff_string = gff_dict[record]['gff']
			gff_lines = gff_string.split('\n')
			for line in gff_lines:
				if not line.startswith('#'):
					line = re.sub(r"\s{2,}", " ", line)
					columns = line.split(' ')
					print columns


if __name__ == "__main__":
	gff_file = sys.argv[1]
	gff_dict = parse_gff_to_dict(gff_file)
	export_files(gff_dict)