## Free text query operations

import sys
import string
import numpy as np
from file_reader import FileReader
from index import global_term
from posting_list import PostingList
from term_weight import TermWeight
from posting_list import inverse_document_frequency as calculate_idf
from index import square_root_of_summation_of_squares

# Represents a query, its operations and results
class Query():
  # terms are dictionary of term and term information from dictionary file
  def __init__(self, query, terms, file_reader, terminizer, document_ids_to_index):
    self.query = query
    self.terms = terms
    self.file_reader = file_reader
    self.terminizer = terminizer
    self.document_ids_to_index = document_ids_to_index
    self.document_index_to_id = dict((v, k) for k, v in document_ids_to_index.iteritems())
    self.document_ids = document_ids_to_index.keys()
    self.number_of_documents = len(document_ids_to_index)
    self.executeQuery()

  # returns a list of document ids results for query
  def getRankedDocumentIds(self):
    return self.results.keys()

  # gets a dictionary of term weights of a term
  def getTermWeights(self, term):
    term_weights = {}
    
    if term in self.terms:
      term_information = self.terms[term]
      line_number = term_information["line_number"]
      line_reader = self.file_reader.getLineReader(line_number)
      line_reader.resetCursor()

      while True:
        line_tuple = line_reader.nextIntFloatTuple()
        if line_tuple == None:
          break
        else:
          document_id = line_tuple[0]
          term_weight = TermWeight(document_id)
          term_weight.setWeight(line_tuple[1])
          term_weights[document_id] = term_weight
        
    return term_weights

  # returns all document indexes
  def getDocumentIds(self):
    return self.document_ids

  # returns document scores
  def getDocumentScores(self):
    return self.results

  # returns ranked documents with scores
  # 0 score documents are not included
  def getRankedDocumentScores(self, limit=10):
    document_ids = self.document_ids
    scores = [self.results[self.document_index_to_id[document_index]] for document_index in range(self.number_of_documents)]
    top_indices = np.argpartition(scores, -limit)[-limit:]
    ranked = [{"document_id" : self.document_index_to_id[top_index], "score": scores[top_index]} for top_index in reversed(top_indices)]
    ranked = filter(lambda document_score: document_score["score"] > 0, ranked)
    print [ds["score"] for ds in ranked]
    return ranked

  # execute query
  def executeQuery(self):
    query_terms = [self.terminizer(token) for token in self.query.split(" ")]
    number_of_documents = self.number_of_documents

    # dummy document id for query posting list
    query_document_id = sys.maxint

    document_vectors = np.zeros((self.number_of_documents, len(query_terms)))
    
    # use posting list for query terms to store frequency information
    # create posting lists for query terms
    # there will only be one entry in each posting list
    query_posting_lists = {}

    # create document vectors
    for term_index, term in enumerate(query_terms):
      term_weights = self.getTermWeights(term)

      for document_id, term_weight in term_weights.items():
        document_index = self.document_ids_to_index[str(document_id)]
        document_vectors[document_index][term_index] = term_weights[document_id].getWeight()

      if not term in query_posting_lists:
        query_posting_lists[term] = PostingList(term)
      query_posting_lists[term].incrementTermFrequency(query_document_id)

    # create query vector
    query_vector = []

    # calculate term weights in query (lnc)
    for term in query_terms:
      query_term_posting_list = query_posting_lists[term]
      document_frequency = self.terms[term]["posting_counts"] if term in self.terms else 0
      inverse_document_frequency = calculate_idf(number_of_documents, document_frequency)
      logarithmic_term_frequency = query_term_posting_list.getTermWeights()[0].getLogarithmicFrequency()
      query_term_weight = logarithmic_term_frequency * inverse_document_frequency
      
      query_vector.append(query_term_weight)
    
    # normalize query vector
    # (sum of w) ^ 1/2
    query_total_weight = square_root_of_summation_of_squares(query_vector)
    query_vector = [query_term_weight / query_total_weight if query_total_weight > 0 else 0 for query_term_weight in query_vector]

    document_scores = {}

    # compute scores for each document
    for document_index, document_vector in enumerate(document_vectors):
      document_length = square_root_of_summation_of_squares(document_vector)
      
      # multiply
      query_document_products = [document_term_weight * query_term_weight for document_term_weight, query_term_weight in zip(document_vector, query_vector)]
      
      # sum
      cosine_similarity = sum(query_document_products)
      document_id = self.document_index_to_id[document_index]
      document_scores[document_id] = cosine_similarity

    self.results = document_scores

if __name__ == "__main__":
  from index import term_from_token
  from index import read_dictionary
  
  filename = 'test_postings.txt'
  file_reader = FileReader(filename)

  dictionary = read_dictionary('test_dictionary.txt')
  terms = dictionary["terms"]
  document_ids = dictionary["document_ids"]
  number_of_documents = len(document_ids)

  query_string = "best"
  query = Query(query_string, terms, file_reader, term_from_token, document_ids)
  print query.getDocumentScores()[1]
  print query.getRankedDocumentScores(4)

  query_string = "car"
  query = Query(query_string, terms, file_reader, term_from_token, document_ids)
  print query.getDocumentScores()[1]
  print query.getRankedDocumentScores(4)

  query_string = "best car insurance"
  query = Query(query_string, terms, file_reader, term_from_token, document_ids)
  print query.getDocumentScores()[1]
  print query.getRankedDocumentScores(4)

  file_reader.close()