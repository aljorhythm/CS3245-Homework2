# Prints dictionary

from index import read_dictionary
import sys

dictionary = read_dictionary(sys.argv[1])

for index, term in enumerate(dictionary):
  print "{}\t{}\t{}".format(index, term[0], term[1])