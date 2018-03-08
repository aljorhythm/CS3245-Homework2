This is the README file for A0000000X's submission

== Python Version ==

I'm (We're) using Python Version <2.7.x or replace version number> for
this assignment.

== General Notes about this assignment ==

1. Indexing
  - Sentence are read from file
  - Sentence is tokenized into word tokens
  - Tokens are stemmed using porter

Experiments
---------------------------------

Storing file as string and without implementing posting lists, the recorded output is:

``````````````````````````````````
➜  CS3245-Homework2 git:(master) ✗ python search.py -d dictionary.txt -p postings.txt -q queries.txt -o output.txt -t
Started at 1520513928.64, ended at 1520513932.88, time taken: 4.2426431179
➜  CS3245-Homework2 git:(master) ✗ ls -l output.txt
-rw-r--r--  1 joellim  staff  464956 Mar  8 20:58 output.txt
``````````````````````````````````

Tests
---------------------------------
Unit Tests are available on some scripts.
Running the script by default runs the test

1. file_reader.py
2. query.py
3. test_postings.txt - contains test postings for testing query algo

Also for printing purposes, the dictionary file can be printed in a readable format using
python print_dictionary.py dictionary.txt

Known Limitations or Bugs
---------------------------------
1. The file reader assumes that line number is always valid
2. The file reader also assumes that a line reader will not be requested
before

== Files included with this submission ==

document.py
- Represents a document object, used during indexing

file_reader.py
- a file reader object that seeks to line positions quickly without reading

index.py
- main indexing file
- contains tokenizer, term processing

line_reader.py
- a line reader to read to and fro a line of postings

posting_list.py
- represents a posting list, used during indexing

print_dictionary.py
- utility method to print readable format from serialized dictionary file, can ignore

== Statement of individual work ==

Please initial one of the following statements.

[x] I, A0000000X, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I, A0000000X, did not follow the class rules regarding homework
assignment, because of the following reason:

<Please fill in>

I suggest that I should be graded as follows:

<Please fill in>

== References ==
