############################################################
# Author: Amanjeev Sethi
# License: MIT
# Usage: At your own risk
# This file is very specific to the needs of this project.
# Please do not attempt to use it without reading this code.
############################################################

import os
import sys
import re
import getopt
import json
import requests

SRA_INTERNAL_URL = os.getenv('SRA_INTERNAL_URL', '')
ASSEMBLY = 'GRCh37'

def get_file_content(filename):
  content = []
  with open(filename) as f:
    content = f.readlines()
  return content

def get_line_fields(content):
  fields = []
  for line in content:
    line = line.rstrip()
    fields_this_line = re.split(r'\t+', line.rstrip('\t\n'))
    fields.append(fields_this_line)
  return fields

def get_all_lines_fields(filename):
  content = get_file_content(filename)
  fields = get_line_fields(content)
  return fields

def write_file(filename, data):
  f = open(filename, 'w')
  f.write(data)
  f.close()

def get_sra_beacon_json(chr, pos, assembly='GRCh37'):
    req = requests.get(SRA_INTERNAL_URL + '?ref=' + assembly + '&chrom=' + chr + '&pos=' + pos)
    print SRA_INTERNAL_URL + '?ref=' + assembly + '&chrom=' + chr + '&pos=' + pos

def get_sra_data(input="", output="~/projects/faes/figs/output/clinvar_sra_data.txt"):
    fields = get_all_lines_fields(input)
    data = 'Accession\tLocation\tChromosome\tA\tC\tG\tT\n'
    for line in fields:
        if line[0] != 'Accession':
            get_sra_beacon_json(line[1], line[2], assembly='GRCh37')
            data += line[0] + '\t' + line[1] + '\t' + line[2] + '\t' + '0' + '\t' + '0' + '\t' + '0' + '\t' + '0' + '\n'
    write_file(output, data)

def usage():
    print "Usage: \n\t python get_sra_data.py <input_file> <output_file>"

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "")
        if len(args) != 2:
            usage()
            sys.exit(2)
        elif len(args) == 2:
            get_sra_data(input=args[0], output=args[1])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])