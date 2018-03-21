
# Line reader
# Can read next int,int tuple in an already opened file
class LineReader():
  def __init__(self, file, start_position):
    self.file = file
    self.start_position = start_position
    self.current_position = self.start_position

  # read all ints on the line
  def allIntTuples(self):
    store_position = self.current_position
    self.resetCursor()
    self.all_ints = self.nextIntTuple()
    self.current_position = store_position
    return self.all_ints

  # reset cursor
  def resetCursor(self):
    self.current_position = self.start_position

  # get next integer on line, return None if end of line
  def nextIntTuple(self):
    nextIntTuple = []
    nextInt = ""
    
    while True:
      self.file.seek(self.current_position)
      nextChar = self.file.read(1)
      self.current_position += 1
      if nextChar is None or nextChar == '\n':
        if nextInt.isdigit():
          nextIntTuple.append(int(nextInt))
        self.current_position -= 1
        break
      elif nextChar.isdigit():
        nextInt += str(int(nextChar, 10))
      elif nextChar == '-':
        nextIntTuple.append(int(nextInt))
        nextInt = ""
      elif nextChar == ' ':
        nextIntTuple.append(int(nextInt))
        break
    
    if nextIntTuple == []:
      return None
    
    return nextIntTuple

  # gets all integers from cursor onwards
  def nextIntTuples(self):
    intTuples = []
    while True:
      next = self.nextIntTuple()
      if next == None:
        break
      intTuples.append(next)
    return intTuples