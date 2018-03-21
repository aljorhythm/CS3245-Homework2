#Represents a term frequency in document

class TermFrequency():
  def __init__(self, id):
    self.frequency = 0
    self.documentId = id
  # increments of frequency of term in document
  def incrementFrequency(self):
    self.frequency += 1
  # returns frequency of term in document
  def getFrequency(self):
    return self.frequency
  # returns document id
  def getDocumentId(self):
    return self.documentId