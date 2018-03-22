# Prints dictionary

from index import read_dictionary
import sys

dictionary_file = sys.argv[1] if len(sys.argv) > 1 else "dictionary.txt"
dictionary = read_dictionary(dictionary_file)

terms = dictionary["terms"]
for term, term_info in terms.items():
  print "{}:\t\t{}\t{}".format(term, term_info["line_number"], term_info["posting_counts"])

print "Number of documents: {}".format(dictionary["meta"]["number_of_documents"])

print dictionary["document_ids_to_index"]