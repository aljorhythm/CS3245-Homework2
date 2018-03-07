
# Line reader
# Reads next in the current line from an already opened file
class LineReader():
  def __init__(self, file, start_position):
    self.file = file
    self.start_position = start_position
    self.current_position = self.start_position
  # read all ints on the line
  def allInts(self):
    store_position = self.current_position
    self.resetCursor()
    self.all_ints = self.nextInts()
    self.current_position = store_position
    return self.all_ints
  # reset cursor
  def resetCursor(self):
    self.current_position = self.start_position
  # get next integer on line, return None if end of line
  def nextInt(self):
    nextInt = ""
    
    while True:
      self.file.seek(self.current_position)
      nextChar = self.file.read(1)
      self.current_position += 1
      if nextChar is None or nextChar == '\n':
        self.current_position -= 1
        break
      try:     
        nextInt += str(int(nextChar, 10))
      except:
        break
    
    if nextInt == "":
      return None
    return int(nextInt, 10)
  # gets all integers from cursor onwards
  def nextInts(self):
    ints = []
    while True:
      next = self.nextInt()
      if next == None:
        break
      ints.append(next)
    return ints