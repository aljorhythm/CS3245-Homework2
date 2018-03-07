import os
import argparse
from index import read_dictionary

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Process some integers.')
  parser.add_argument('-d', dest='dictionary_file', help='no dictionary file')
  parser.add_argument('-p', dest='postings_file', help='no postings file')
  parser.add_argument('-q', dest='queries_filename', help='no queries file')
  parser.add_argument('-o', dest='results_filename', help='no results file')
  args = parser.parse_args()
  args = vars(args)

  dictionary_file = args["dictionary_file"]
  queries_filename = args["queries_filename"]
  postings_file = args["postings_file"]
  results_filename = args["results_filename"]

  dictionary = read_dictionary(dictionary_file)
  print dictionary