# A single posting list
# Associated with a term
class PostingList():
  def __init__(self, term):
    self.term = term
    self.documents = []
  def getCount(self):
    return len(self.getDocumentIds())
  def getTerm(self):
    return self.term
  # adds a document and keeps list sorted by document id
  def addDocument(self, document):
    self.documents.append(document)
  # sorted posting list, unique set of document ids
  def getDocumentIds(self):
    return sorted(set(self.documents), key=lambda document: int(document.getId(), 10))
