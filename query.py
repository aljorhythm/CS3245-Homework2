## Query operations
## Shunting algo, merging lists

from file_reader import FileReader
import string
from index import global_term

# operator and precedence
# larger number is higher precedence
query_operators = {
  '(' : 3,
  ')' : 3,
  'NOT' : 2,
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

# generic or operation of two posting lists
# posting_list_2 is global list
# posting_list_1 is subset
# returns all elements in global list but not in subset
# returns a list
def query_not(posting_list_1, posting_list_2):
  posting_1_compare = posting_list_1.nextInt()
  posting_2_compare = posting_list_2.nextInt()

  answer = []

  while posting_1_compare != None and posting_2_compare != None:
    if posting_1_compare == posting_2_compare:
      posting_1_compare = posting_list_1.nextInt()
      posting_2_compare = posting_list_2.nextInt()
    else:
      if posting_1_compare > posting_2_compare:
        answer.append(posting_2_compare)        
        posting_2_compare = posting_list_2.nextInt()
      else:
        posting_1_compare = posting_list_1.nextInt()

  while posting_2_compare != None:
    answer.append(posting_2_compare)
    posting_2_compare = posting_list_2.nextInt()
        
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
  # terms are dictionary of term and term information from dictionary file
  def __init__(self, query, terms, file_reader, terminizer):
    self.query = query
    self.terms = terms
    self.file_reader = file_reader
    self.terminizer = terminizer
    self.executeQuery()

  # ensures that operand is posting list that has a nextInt() method.
  # if operand is a term the list will be retrieved after transforming it to a term
  # if term is not in dictionary a empty list is returned
  def operandToPostingList(self, tokenOrList):
    if isinstance(tokenOrList, list):
      return NextableIntList(tokenOrList)
    
    term = self.terminizer(tokenOrList)

    if term not in self.terms:
      return NextableIntList([])
    line_number = self.terms[term]["line_number"]
    return self.file_reader.getLineReader(line_number)
    
  # generic operation, handles automatically if operands(s) are token or result
  def operation(self, operand_1, operator, operand_2=None):
    operand_1 = self.operandToPostingList(operand_1)
    operand_2 = global_term if operator.upper() == "NOT" else operand_2
    operand_2 = self.operandToPostingList(operand_2)
    if operand_1 == operand_2:
      return query_or(operand_1, self.operandToPostingList([]))
    if operator.lower() == 'and':
      return query_and(operand_1, operand_2)  
    elif operator.lower() == 'or':
      return query_or(operand_1, operand_2)
    elif operator.lower() == 'not':
      return query_not(operand_1, operand_2)
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
      is_operand = not is_operator

      if is_operand:
        operands.append(operand_or_operator)
      elif operand_or_operator == '(':
        operators.append(operand_or_operator)
      elif is_operator and not is_parenthesis:
        while True:
          operators_len = len(operators)
          if operators_len == 0 or (get_operator_precedence(operators[-1]) >= operator_precedence) or operand_or_operator.lower() == 'not':
            if operators_len > 0 and operators[-1].lower() == 'not':
              operator = operators.pop()
              operand_1 = operands.pop()
              calculation = self.operation(operand_1, operator, None)
              operands.append(calculation)
            operators.append(operand_or_operator)
            break

          operator = operators.pop()
          operand_1 = operands.pop()
          operand_2 = operands.pop() if operator.upper() != "NOT" else None
          calculation = self.operation(operand_1, operator, operand_2)
          operands.append(calculation)
      elif operand_or_operator == ')':
        while True:
          if operators_len == 0 or (get_operator_precedence(operators[-1]) >= operator_precedence):
            break
          operator = operators.pop()
          operand_1 = operands.pop()
          operand_2 = operands.pop() if operator.upper() != "NOT" else None
          calculation = self.operation(operand_1, operator, operand_2)
          operands.append(calculation)
      
      operand_or_operator = ""

    while len(operators) > 0:
        operator = operators.pop()
        if operator == '(':
          continue
        operand_1 = operands.pop()
        operand_2 = operands.pop() if operator.upper() != "NOT" else None
        calculation = self.operation(operand_1, operator, operand_2)
        operands.append(calculation)

    assert len(operands) == 1, "Syntax wrong '{}' {}".format(self.query, operands)

    results = operands[0]
    if results is not list:
      posting_list = self.operandToPostingList(results)
      results = []
      while True:
        nextInt = posting_list.nextInt()
        if nextInt is None:
          break
        results.append(nextInt)
    self.results = results

if __name__ == "__main__":
  from index import term_from_token
  from index import dictionary_list_to_dict
  
  assert query_or(NextableIntList([1]), NextableIntList([1])) == [1]
  assert query_and(NextableIntList([1, 2]), NextableIntList([1, 2])) == [1, 2]

  filename = 'test_postings.txt'
  file_reader = FileReader(filename)
  terms = [('x', 4), ('y', 3), ('z', 2), ('third', 3), ('fourth', 3), ('fifth', 2), ('', 10), ('x2', 4)]
  terms = dictionary_list_to_dict(terms)

  query_string = 'not x and x'
  query = Query(query_string, terms, file_reader, term_from_token)
  assert query.getDocumentIds() == [], query.getDocumentIds()

  query_string = 'x or not x and x'
  query = Query(query_string, terms, file_reader, term_from_token)
  assert query.getDocumentIds() == [1, 4, 6, 9], query.getDocumentIds()

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

  query_string = 'fifth and (third or fourth) and fifth'  
  query = Query(query_string, terms, file_reader, term_from_token)
  assert query.getDocumentIds() == [2, 6], query.getDocumentIds()

  query_string = 'fifth or z and (third or fourth)'
  query = Query(query_string, terms, file_reader, term_from_token)
  assert query.getDocumentIds() == [2, 4, 6], query.getDocumentIds()

  query_string = 'not x'
  query = Query(query_string, terms, file_reader, term_from_token)
  assert query.getDocumentIds() == [2, 3, 5, 7, 8, 10], query.getDocumentIds()

  query_string = 'x or not x'
  query = Query(query_string, terms, file_reader, term_from_token)
  assert query.getDocumentIds() == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], query.getDocumentIds()

  query_string = 'x and x2'
  query = Query(query_string, terms, file_reader, term_from_token)
  assert query.getDocumentIds() == [1, 4, 6, 9], query.getDocumentIds()

  query_string = 'x and x'
  query = Query(query_string, terms, file_reader, term_from_token)
  assert query.getDocumentIds() == [1, 4, 6, 9], query.getDocumentIds()

  query_string = 'not (x and x)'
  query = Query(query_string, terms, file_reader, term_from_token)
  assert query.getDocumentIds() == [2, 3, 5, 7, 8, 10], query.getDocumentIds()

  query_string = 'a'
  query = Query(query_string, terms, file_reader, term_from_token)
  assert query.getDocumentIds() == [], query.getDocumentIds()

  query_string = 'z'
  query = Query(query_string, terms, file_reader, term_from_token)
  assert query.getDocumentIds() == [4, 6], query.getDocumentIds()

  query_string = 'a and z'
  query = Query(query_string, terms, file_reader, term_from_token)
  assert query.getDocumentIds() == [], query.getDocumentIds()

  query_string = 'a or z'
  query = Query(query_string, terms, file_reader, term_from_token)
  assert query.getDocumentIds() == [4, 6], query.getDocumentIds()

  