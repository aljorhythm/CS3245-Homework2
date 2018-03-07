from file_reader import FileReader

# Represents a query, its operations and results
class Query():
  # terms are dictionary of term and term information pairs
  def __init__(self, query, terms, file_reader, tokenizer):
    self.query = query
    self.terms = terms
    self.file_reader = file_reader
    self.tokenizer = tokenizer

  # do an and query and returns an array of document ids
  def queryAnd(self, token1, token2):
    term1 = self.tokenizer(token1)
    term1_line_number = self.terms[term1]["line_number"]
    postings_1_line_reader = file_reader.getLineReader(term1_line_number)    
    
    term2 = self.tokenizer(token2)
    term2_line_number = self.terms[term2]["line_number"]
    postings_2_line_reader = file_reader.getLineReader(term2_line_number)

    posting_1_compare = postings_1_line_reader.nextInt()
    posting_2_compare = postings_2_line_reader.nextInt()

    answer = []

    while posting_1_compare != None and posting_2_compare != None:
      if posting_1_compare == posting_2_compare:
        answer.append(posting_1_compare)
        posting_1_compare = postings_1_line_reader.nextInt()
        posting_2_compare = postings_2_line_reader.nextInt()
      else:
        if posting_1_compare < posting_2_compare:
          posting_1_compare = postings_1_line_reader.nextInt()
        else:
          posting_2_compare = postings_2_line_reader.nextInt()
    return answer

  # do an and query and returns an array of document ids
  def queryOr(self, token1, token2):
    term1 = self.tokenizer(token1)
    term1_line_number = self.terms[term1]["line_number"]
    postings_1_line_reader = file_reader.getLineReader(term1_line_number)    
    
    term2 = self.tokenizer(token2)
    term2_line_number = self.terms[term2]["line_number"]

    postings_2_line_reader = file_reader.getLineReader(term2_line_number)

    posting_1_compare = postings_1_line_reader.nextInt()
    posting_2_compare = postings_2_line_reader.nextInt()

    answer = []

    while True:
      if posting_1_compare is None and posting_2_compare is None:
        break
      if posting_1_compare is posting_1_compare == posting_2_compare:
        answer.append(posting_1_compare)
        posting_1_compare = postings_1_line_reader.nextInt()
        posting_2_compare = postings_2_line_reader.nextInt()
        continue
      while (posting_1_compare is None or posting_1_compare > posting_2_compare) and posting_2_compare is not None:
        answer.append(posting_2_compare)
        posting_2_compare = postings_2_line_reader.nextInt()
        if posting_2_compare is None:
          break
      answer.append(posting_1_compare)
      posting_1_compare = postings_1_line_reader.nextInt()

    return answer

  # returns an array of document ids for query
  def getDocuments(documents):
    return []

if __name__ == "__main__":
  from index import term_from_token
  from index import dictionary_list_to_dict
  filename = 'test_postings.txt'
  file_reader = FileReader(filename)
  terms = [('x', 1), ('y', 2), ('z', 3)]
  terms = dictionary_list_to_dict(terms)
  query_string = 'x or y'
  query = Query(query_string, terms, file_reader, term_from_token)
  assert query.queryAnd('x', 'y') == [1]
  print query.queryOr('x', 'y')
  
  assert query.queryOr('x', 'y') == [1, 3, 4, 6, 8, 9]