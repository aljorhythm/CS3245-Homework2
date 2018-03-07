class PostingList():
  def __init__(self, token):
    self.token = token
    self.documents = []
  def getCount(self):
    return len(self.documents)
  def getToken(self):
    return self.token
  # adds a document and keeps list sorted by document id
  def addDocument(self, document):
    self.documents.append(document)
  # sorted posting list
  def getDocuments(self):
    return sorted(set(self.documents), key=lambda document: document.getId())
