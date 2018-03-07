import os
import argparse
from index import read_dictionary

# returns array of queries
def read_queries(filename):
  with open(filename) as file:
    return file.readlines()

# returns search results of query
def search(query, dictionary, posting_file):
  return

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Process some integers.')
  parser.add_argument('-d', dest='dictionary_filename', help='no dictionary file')
  parser.add_argument('-p', dest='postings_filename', help='no postings file')
  parser.add_argument('-q', dest='queries_filename', help='no queries file')
  parser.add_argument('-o', dest='results_filename', help='no results file')
  args = parser.parse_args()
  args = vars(args)

  dictionary_filename = args["dictionary_filename"]
  queries_filename = args["queries_filename"]
  postings_filename = args["postings_filename"]
  results_filename = args["results_filename"]

  queries = read_queries(queries_filename)
  dictionary = read_dictionary(dictionary_file)

  query = queries[0]
  search_result = search(query, dictionary, postings_filename)
  print search_result