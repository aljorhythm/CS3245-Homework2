## Download Reuters Corpora

```
➜  CS3245-Homework2 git:(master) ✗ python
Python 2.7.10 (default, Jul 15 2017, 17:16:57)
[GCC 4.2.1 Compatible Apple LLVM 9.0.0 (clang-900.0.31)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import nltk
>>> nltk.download('reuters')
[nltk_data] Downloading package reuters to /Users/joellim/nltk_data...
[nltk_data]   Package reuters is already up-to-date!
True
```

## Running

`python index.py -i directory-of-documents -d dictionary-file -p postings-file`
`python index.py -i .../nltk_data/corpora/reuters/training/ -d dictionary.txt -p postings.txt`
`python index.py -i /home/course/cs3245/nltk_data/corpora/reuters/training/ -d dictionary.txt -p postings.txt`