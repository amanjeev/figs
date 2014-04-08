import sys
import re


def get_file_content(filename):
  content = []
  with open(filename) as f:
    content = f.readlines()
  return content

def get_line_fields(content):
  fields = []
  for line in content:
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

def main_snp(param, filename):
  if param == 'snp':
    get_snp(filename)
  elif param == 'acc':
    get_acc(filename)
  else:
    get_both(filename)

def get_snp(filename):
  fields = get_all_lines_fields(filename)
  data = 'dbSNP ID'
  for line in fields:
    if line[-1] != 'dbSNP':
      data += str(line[-1]) + '\n'
  write_file('/home/scidb/proj/figs/figs/data_heart/clinvar_dbsnp_id_only_heart_disease.txt', data)

def get_acc(filename):
  print 'Just accession has not been implemented yet and we probably do not need it'

def get_both(filename):
  fields = get_all_lines_fields(filename)
  data = 'ClinVar Accession\tdbSNP ID\n'
  for line in fields:
    if line[-1] != 'dbSNP' and line[-2] != 'Accession':
      data += line[-2] + '\t' + line[-1] + '\n'
  write_file('/home/scidb/proj/figs/figs/data_heart/clinvar_dbsnp_id_cv_accession_heart_disease.txt', data)
  
def usage():
  print "\nGive what you want:"
  print "snp: snp ids; acc: clinvar accession; snpacc: both;"

def main(argv):
  if len(argv) != 2:
    usage()
    sys.exit(2)
  elif len(argv) == 2:
    script, param = argv
    filename = '/home/scidb/proj/figs/figs/data_heart/clinvar_result_tabbed_file_dbsnp_heart_disease.txt'
    main_snp(param, filename)
  else:
    print "something is wrong and we do not know what is wrong"
    sys.exit(2)

if __name__ == '__main__':
  main(sys.argv)