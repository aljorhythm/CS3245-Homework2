# create test data according to week 7 slides
import os

# create first file
filename = "test_data/{}".format(1)
with open(filename, 'w') as file:
    file.write('car insurance auto insurance')

# create other files
for i in range(2, 5001):
  filename = "test_data/{}".format(str(i))
  with open(filename, 'w') as file:
    file.write('auto')

# create other files
for i in range(5001, 5001 + 50000):
  filename = "test_data/{}".format(str(i))
  with open(filename, 'w') as file:
    file.write('best')

# create other files
for i in range(5001 + 50000, 5001 + 50000 + 10000):
  filename = "test_data/{}".format(str(i))
  with open(filename, 'w') as file:
    file.write('car')

# create other files
for i in range(5001 + 50000 + 10000, 5001 + 50000 + 10000 + 1000):
  filename = "test_data/{}".format(str(i))
  with open(filename, 'w') as file:
    file.write('insurance')