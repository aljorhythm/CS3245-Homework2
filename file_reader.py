
# Line reader for postings
class LineReader():
  def __init__(self, file, start_position):
    self.file = file
    self.start_position = start_position
    self.current_position = start_position
  def nextInt(self):
    nextInt = ""
    while True:
      self.file.seek(self.current_position)
      self.current_position += 1
      nextChar = self.file.read(1)
      try:
        nextInt += str(int(nextChar, 10))
      except:
        break
    return int(nextInt, 10)
    
# File reader for postings
# current_line_starting_position is always at the beginning of the line
class FileReader():
  def __init__(self, filepath):
    self.file = open(filepath, 'r')
    self.line_number = 1
    self.current_line_starting_position = 0
  # returns current line that is read, 1-based
  def getCurrentLineNumber(self):
    return self.line_number
  # returns current line reader
  def getCurrentLineReader(self):
    return LineReader(self.file, self.current_line_starting_position)
  def close(self):
    self.file.close()

if __name__ == "__main__":
  file_reader = FileReader('postings.txt')
  assert file_reader.getCurrentLineNumber() == 1
  line_reader = file_reader.getCurrentLineReader()
  assert isinstance(line_reader.nextInt(), int)
  file_reader.close()