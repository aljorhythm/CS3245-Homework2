from line_reader import LineReader

# File reader for postings
# Seeks line by line
# current_line_starting_position is always at the beginning of the line
# line readers are initiated on seek, even if the line is not the target
class FileReader():
  def __init__(self, filepath):
    self.file = open(filepath, 'r')
    self.line_number = 1
    self.current_line_starting_position = 0
    self.line_readers = {}

  # if line reader doesn't exist, seek to line and create one
  # assumes that current
  # line reader is always reset, do not use concurrently between two operations
  def getLineReader(self, line_number):
    if not line_number in self.line_readers:
      while True:
        line_reader = LineReader(self.file, self.current_line_starting_position)
        self.line_readers[self.getCurrentLineNumber()] = line_reader
        if self.getCurrentLineNumber() == line_number:
          break
        self.seekNextLine()
    line_reader = self.line_readers[line_number]
    
    line_reader.resetCursor()
    return line_reader

  # returns current line that is read, 1-based
  def getCurrentLineNumber(self):
    return self.line_number

  # sets cursor to next line
  def seekNextLine(self):
    cursor = self.current_line_starting_position
    while True:
      self.file.seek(cursor)
      nextChar = self.file.read(1)
      cursor += 1
      if nextChar == '\n':
        break
    self.current_line_starting_position = cursor
    self.line_number += 1

  # returns current line reader
  def getCurrentLineReader(self):
    return self.getLineReader(self.getCurrentLineNumber())
  
  # close
  def close(self):
    self.file.close()

if __name__ == "__main__":
  file_reader = FileReader('test_postings.txt')
  assert file_reader.getCurrentLineNumber() == 1
  line_reader = file_reader.getCurrentLineReader()

  assert line_reader.nextInt() == 1
  assert line_reader.nextInt() == 4
  assert line_reader.nextInt() == 6
  assert line_reader.nextInt() == 9
  assert line_reader.nextInt() == None
  assert line_reader.nextInt() == None
  assert file_reader.getCurrentLineNumber() == 1

  file_reader.seekNextLine()
  assert file_reader.getCurrentLineNumber() == 2

  line_reader_3 = file_reader.getLineReader(3)
  assert line_reader_3.nextInt() == 4
  assert line_reader_3.nextInt() == 6
  assert line_reader_3.nextInt() == None
  assert line_reader_3.nextInt() == None

  line_reader_2 = file_reader.getLineReader(2)
  
  assert line_reader_2.nextInts() == [1, 3, 8]
  
  file_reader.close()