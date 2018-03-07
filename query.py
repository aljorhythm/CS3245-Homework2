from file_reader import FileReader
import string

# operator and precedence
# larger number is higher precedence
query_operators = {
  'AND' : 1,
  'OR' : 0
}

# Utility so that we can use merge algo on a list of integers
class NextableIntList():
  def __init__(self, ints):
    self.ints = ints
    self.cursor = 0
  def nextInt(self):
    if self.cursor == len(self.ints):
      return None
    ret = self.ints[self.cursor]
    self.cursor += 1
    return ret

# generic or operation of two posting lists
# returns a list
def query_or(posting_list_1, posting_list_2):
  posting_1_compare = posting_list_1.nextInt()
  posting_2_compare = posting_list_2.nextInt()

  answer = []

  while True:
    if posting_1_compare is None and posting_2_compare is None:
      break
    if posting_1_compare == posting_2_compare:
      answer.append(posting_1_compare)
      posting_1_compare = posting_list_1.nextInt()
      posting_2_compare = posting_list_2.nextInt()
      continue
    while (posting_1_compare is None or posting_1_compare > posting_2_compare) and posting_2_compare is not None:
      answer.append(posting_2_compare)
      posting_2_compare = posting_list_2.nextInt()
      if posting_2_compare is None:
        break
    if posting_1_compare is not None:
      answer.append(posting_1_compare)
      posting_1_compare = posting_list_1.nextInt()

  return answer

# generic and operation of two posting lists
# returns a list
def query_and(posting_list_1, posting_list_2):
  posting_1_compare = posting_list_1.nextInt()
  posting_2_compare = posting_list_2.nextInt()

  answer = []

  while posting_1_compare != None and posting_2_compare != None:
    if posting_1_compare == posting_2_compare:
      answer.append(posting_1_compare)
      posting_1_compare = posting_list_1.nextInt()
      posting_2_compare = posting_list_2.nextInt()
    else:
      if posting_1_compare < posting_2_compare:
        posting_1_compare = posting_list_1.nextInt()
      else:
        posting_2_compare = posting_list_2.nextInt()
  return answer

# returns if is parenthesis
def unit_is_parenthesis(unit):
  return unit in ['(', ')']

# returns None if unit is not an operator
def get_operator_precedence(unit):
  unit = unit.upper()
  return query_operators[unit] if unit in query_operators else None

# Represents a query, its operations and results
class Query():
  # terms are dictionary of term and term information pairs
  def __init__(self, query, terms, file_reader, tokenizer):
    self.query = query
    self.terms = terms
    self.file_reader = file_reader
    self.tokenizer = tokenizer
    self.executeQuery()

  # ensures that operand is posting list that has a hasNextInt() method.
  # if operand is a token the list will be retrieved after transforming it to a term
  def operandToPostingList(self, tokenOrList):
    if isinstance(tokenOrList, list):
      return NextableIntList(tokenOrList)
    term = self.tokenizer(tokenOrList)
    line_number = self.terms[term]["line_number"]
    return file_reader.getLineReader(line_number)
    
  # generic operation, handles automatically if operands(s) are token or result
  def operation(self, operand_1, operator, operand_2):
    operand_1 = self.operandToPostingList(operand_1)
    operand_2 = self.operandToPostingList(operand_2)
    if operator.lower() == 'and':
      return query_and(operand_1, operand_2)  
    elif operator.lower() == 'or':
      return query_or(operand_1, operand_2)
    else:
      assert False, operator

  # returns a list of document ids results for query
  def getDocumentIds(self):
    return self.results

  # execute query
  # shunting algo
  # https://stackoverflow.com/questions/13421424/how-to-evaluate-an-infix-expression-in-just-one-scan-using-stacks
  def executeQuery(self):
    operands = []
    operators = []
    operand_or_operator = ""

    query = self.query + ' '
    query = string.replace(query, '(', ' ( ')
    query = string.replace(query, ')', ' ) ')
    for char in list(query):
      if char != ' ':
        if char in ['(', ')']:
          operand_or_operator += char
        else:
          operand_or_operator += char
          continue
      if operand_or_operator == '':
        continue

      operator_precedence = get_operator_precedence(operand_or_operator)

      is_operator = operator_precedence != None
      is_parenthesis = unit_is_parenthesis(operand_or_operator)
      is_operand = not is_operator and not is_parenthesis

      if is_operand:
        operands.append(operand_or_operator)
      elif operand_or_operator == '(':
        operators.append(operand_or_operator)
      elif is_operator:
        while True:
          operators_len = len(operators)
          if operators_len == 0 or (operators_len > 0 and (unit_is_parenthesis(operators[-1]) or get_operator_precedence(operators[-1]) < operator_precedence)):
            operators.append(operand_or_operator)
            break
          operator = operators.pop()
          operand_1 = operands.pop()
          operand_2 = operands.pop()
          calculation = self.operation(operand_1, operator, operand_2)
          operands.append(calculation)
      elif operand_or_operator == ')':
        while len(operands) > 1:
          if len(operators) > 0 and get_operator_precedence(operators[-1]) < operator_precedence:
            break
          if len(operators) > 0 and unit_is_parenthesis(operators[-1]):
            operators.pop()
            break
          operator = operators.pop()
          operand_1 = operands.pop()
          operand_2 = operands.pop()
          calculation = self.operation(operand_1, operator, operand_2)
          operands.append(calculation)
      
      operand_or_operator = ""

    while len(operators) > 0 and len(operands) > 1:
        operator = operators.pop()
        operand_1 = operands.pop()
        operand_2 = operands.pop()
        calculation = self.operation(operand_1, operator, operand_2)
        operands.append(calculation)

    assert len(operands) == 1, "Syntax wrong"
    self.results = operands[0]

if __name__ == "__main__":
  from index import term_from_token
  from index import dictionary_list_to_dict
  
  assert query_or(NextableIntList([1]), NextableIntList([1])) == [1]

  filename = 'test_postings.txt'
  file_reader = FileReader(filename)
  terms = [('x', 4), ('y', 3), ('z', 2), ('third', 3), ('fourth', 3), ('fifth', 2)]
  terms = dictionary_list_to_dict(terms)

  query_string = 'x and y'
  query = Query(query_string, terms, file_reader, term_from_token)
  assert query.getDocumentIds() == [1], query.getDocumentIds()

  query_string = 'x or y'
  query = Query(query_string, terms, file_reader, term_from_token)
  assert query.getDocumentIds() == [1, 3, 4, 6, 8, 9], query.getDocumentIds()

  query_string = '(third or fourth) and fifth'
  query = Query(query_string, terms, file_reader, term_from_token)
  assert query.getDocumentIds() == [2, 6], query.getDocumentIds()

  query_string = 'fifth and (third or fourth)'
  query = Query(query_string, terms, file_reader, term_from_token)
  assert query.getDocumentIds() == [2, 6], query.getDocumentIds()

  query_string = 'fifth or z and (third or fourth)'
  query = Query(query_string, terms, file_reader, term_from_token)
  assert query.getDocumentIds() == [2, 4, 6], query.getDocumentIds()