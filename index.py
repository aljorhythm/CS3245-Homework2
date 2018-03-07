import argparse
import os
from itertools import chain
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from posting_list import PostingList
from document import Document
try:
    import cPickle as pickle
except:
    import pickle

ps = PorterStemmer()

# returns tuples of training filepaths and their corresponding ids from a directory
def get_training_filepaths_and_ids(directory_of_documents, limit=None):
  filenames_all = []
  for (dirpath, dirnames, filenames) in os.walk(directory_of_documents):
    if limit is not None:
      filenames = filenames[0:limit]
    filenames_all.extend([(os.path.join(dirpath, filename), filename) for filename in filenames])
    break
  return filenames_all

# get tokens from file
# operations are sentence tokenizing, word tokenizing, case folding then stem
def tokens_from_file(filepath):
  with open(filepath) as file:
    return map(lambda x: ps.stem(x.lower()) ,list(chain.from_iterable([word_tokenize(sentence) for sentence in sent_tokenize(file.read())])))

# returns dict of vocabulary and corresponding posting list
# can introduce a limit to the number of documents
def retrieve_posting_lists(training_directory, documents_limit=None):
  training_filepaths_and_ids = get_training_filepaths_and_ids(training_directory, documents_limit)
  posting_lists = {}
  for training_filepath_and_id in training_filepaths_and_ids:
    training_filepath, id = training_filepath_and_id
    tokens = tokens_from_file(training_filepath)
    document = Document(id, training_filepath)
    for token in tokens:
      if not token in posting_lists:
        posting_lists[token] = PostingList(token)
      posting_lists[token].addDocument(document)
  return posting_lists

# writes postings lists to file
def write_posting_lists(filename, posting_lists):
  with open(filename, 'w') as file:
    print [" ".join([document.getId() for document in posting_list.getDocuments()]) for posting_list in posting_lists]
    file.writelines([" ".join([document.getId() for document in posting_list.getDocuments()]) + "\n" for posting_list in posting_lists])

# accepts a dictionary of posting lists
# returns a sorted array of posting lists which is consistent in dictionary and posting list file
def sorted_array_posting_list(posting_lists):
  return [posting_lists[key] for key in sorted(posting_lists.keys())]

# accepts a sorted array of posting lists, see sorted_array_posting_list()
# write dictionary
def write_dictionary(filename, posting_lists):
  with open(filename, 'w') as file:
    data = [(posting_list.getToken(), posting_list.getCount()) for posting_list in posting_lists]
    serialized = pickle.dumps(data)
    file.write(serialized)

# accepts a sorted array of posting lists, see sorted_array_posting_list()
# returns a sorted array of posting lists
def read_dictionary(filename):
  with open(filename, 'r') as file:
    serialized = file.read()
    return pickle.loads(serialized)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Process some integers.')
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

  posting_lists = retrieve_posting_lists(directory_of_documents, documents_limit)
  sorted_posting_lists = sorted_array_posting_list(posting_lists)
  write_posting_lists(postings_file, sorted_posting_lists)
  write_dictionary(dictionary_file, sorted_posting_lists)