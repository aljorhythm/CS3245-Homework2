from term_frequency import TermFrequency

# A single posting list
# Associated with a term and its frequencies in documents
class PostingList():
  def __init__(self, term):
    self.term = term
    self.term_frequencies = {}
  def getDocumentFrequency(self):
    return len(self.term_frequencies)
  # Get term associated with this posting list
  def getTerm(self):
    return self.term
  # increment term frequency in document
  def incrementTermFrequency(self, documentId):
    if not documentId in self.term_frequencies:
      self.term_frequencies[documentId] = TermFrequency(documentId)
    self.term_frequencies[documentId].incrementFrequency()
  # returns a posting list of term frequencies
  def getTermFrequencies(self):
    self.documentIds = self.term_frequencies.keys()
    return [self.term_frequencies[documentId] for documentId in sorted(self.documentIds)]
