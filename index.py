# indexing script

import math
import argparse
import os
from itertools import chain
from posting_list import PostingList
from document import Document
try:
    import cPickle as pickle
except:
    import pickle
import struct

try:
  from nltk.stem import PorterStemmer
  from nltk.tokenize import sent_tokenize, word_tokenize
  ps = PorterStemmer()
  # transform term into token
  def term_from_token(token):
    after = ps.stem(token.lower())
    return after
except:
  # transform term into token
  def term_from_token(token):
    return token

  # sent_tokenize
  def sent_tokenize(sentences):
    return sentences.split(".")

  # word_tokenize
  def word_tokenize(sentence):
    return sentencegit .split(" ")

# Term that will return all documents
global_term = ''

# (w1 ^ 2 + w2 ^ 2 + ... + wN ^ 2) ^ 1/2
def square_root_of_summation_of_squares(ws):
  try:
    return pow(sum([pow(w, 2) for w in ws]), 0.5)
  except:
    return 0

# transform tokens into terms
def terms_from_tokens(tokens):
  return map(term_from_token, tokens)

# get terms from file
# operations are sentence tokenizing, word tokenizing, case folding then stem
def terms_from_file(filepath):
  with open(filepath) as file:
    tokens = list(chain.from_iterable([word_tokenize(sentence) for sentence in sent_tokenize(file.read())]))
    terms = terms_from_tokens(tokens)
    return terms

# returns tuples of training filepaths and their corresponding ids from a directory
def get_training_filepaths_and_ids(directory_of_documents, limit=None, filter=None):
  filenames_all = []
  for (dirpath, dirnames, filenames) in os.walk(directory_of_documents):
    if limit is not None:
      filenames = filenames[0:limit]
    if filter is not None:
      filenames = [filename for filename in filenames if filename == filter]
    filenames_all.extend([(os.path.join(dirpath, filename), filename) for filename in filenames])
    break
  return filenames_all

# writes postings lists to file
def write_posting_lists(filename, indexer):
  posting_lists = indexer.sorted_posting_lists
  document_lengths = indexer.document_lengths
  # by writing string
  with open(filename, 'w') as file:
    file.writelines([" ".join(["{0}-{1}".format(term_weight.getDocumentId(), term_weight.getNormalizedLogarithmicFrequency(document_lengths[term_weight.getDocumentId()])) for term_weight in posting_list.getTermWeights()]) + "\n" for posting_list in posting_lists])

# accepts a sorted array of posting lists, see sorted_array_posting_list()
# write terms and other information to dictionary
def write_dictionary(filename, indexer):
  posting_lists = indexer.sorted_posting_lists
  number_of_documents = indexer.number_of_documents
  meta = { "number_of_documents": number_of_documents }
  terms = [(posting_list.getTerm(), posting_list.getDocumentFrequency()) for posting_list in posting_lists]
  document_lengths = indexer.document_lengths
  document_ids = sorted(document_lengths.keys(), key=lambda id_string: int(id_string))
  document_ids_to_index = {}
  for index, document_id in enumerate(document_ids):
    document_ids_to_index[document_id] = index

  with open(filename, 'w') as file:
    data = {
      "meta" : meta,
      "terms" : dictionary_list_to_dict(terms),
      "document_lengths" : document_lengths,
      "document_ids_to_index" : document_ids_to_index
    }
    serialized = pickle.dumps(data)
    file.write(serialized)

# accepts a sorted array of dictionary term information, see sorted_array_posting_list()
# returns a sorted array of dictionary term information
def read_dictionary(filename):
  with open(filename, 'r') as file:
    serialized = file.read()
    return pickle.loads(serialized)

# used in write_dictionary() to convert terms information into dictionary
def dictionary_list_to_dict(dictionary_list):
  dict_representation = {}
  for index, term in enumerate(dictionary_list):
    dict_representation[term[0]] = { "line_number" : index + 1, "posting_counts" : term[1] }
  return dict_representation

# Represents construction of the dictionary and posting list
# lnc scheme is used for posting lists
class Indexer():
  def __init__(self, directory_of_documents, documents_limit=None):
    self.number_of_documents = 0
    self.posting_lists, self.document_lengths = self.retrieve_posting_lists_and_document_lengths(directory_of_documents, documents_limit)
    self.sorted_posting_lists = self.sorted_array_posting_list(self.posting_lists)

  # returns dict of vocabulary and corresponding posting list
  # can introduce a limit to the number of documents
  # counts the number of documents, if limit exists it will be used as number of documents
  # posting list
  def retrieve_posting_lists_and_document_lengths(self, training_directory, documents_limit=None):
    training_filepaths_and_ids = get_training_filepaths_and_ids(training_directory, documents_limit)
    training_filepaths_and_ids = sorted(training_filepaths_and_ids, key=lambda x: int(x[1], 10))

    document_lengths = {}
    
    self.number_of_documents = documents_limit if documents_limit is not None else len(training_filepaths_and_ids)

    posting_lists = {}

    for training_filepath_and_id in training_filepaths_and_ids:
      training_filepath, document_id = training_filepath_and_id

      # get terms from document
      terms = terms_from_file(training_filepath)

      document_posting_lists = {}

      # add each term to posting list
      for term in terms:
        if not term in posting_lists:
          posting_lists[term] = PostingList(term)
        posting_lists[term].incrementTermFrequency(document_id)
        document_posting_lists[term] = posting_lists[term]

      # count terms in document
      document_term_counts = []

      # logarthmic counting
      for term, posting_list in document_posting_lists.items():
        document_term_counts.append(posting_list.getDocumentTermWeight(document_id).getLogarithmicFrequency())
      
      # normalized document length
      document_lengths[document_id] = square_root_of_summation_of_squares(document_term_counts)
    return (posting_lists, document_lengths)

  # accepts a dictionary of posting lists
  # returns a sorted array of posting lists which is consistent in dictionary and posting list file
  def sorted_array_posting_list(self, posting_lists):
    return [posting_lists[key] for key in sorted(posting_lists.keys())]

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Indexing')
  parser.add_argument('-i', dest='directory_of_documents', help='no directory')
  parser.add_argument('-d', dest='dictionary_file', help='no dictionary file')
  parser.add_argument('-p', dest='postings_file', help='no postings file')
  parser.add_argument('-l', dest='documents_limit', nargs='?', type=int, default=None, help='documents limit, used for testing/ trials')
  args = parser.parse_args()
  args = vars(args)

  dictionary_file = args["dictionary_file"]
  directory_of_documents = args["directory_of_documents"]
  postings_file = args["postings_file"]
  documents_limit = args["documents_limit"]

  indexer = Indexer(directory_of_documents, documents_limit)

  write_posting_lists(postings_file, indexer)
  write_dictionary(dictionary_file, indexer)