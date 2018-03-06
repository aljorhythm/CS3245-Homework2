import pickle
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-i', dest='directory_of_documents', help='no directory')
parser.add_argument('-d', dest='dictionary_file', help='no dictionary file')
parser.add_argument('-p', dest='postings_file', help='no postings file')
args = parser.parse_args()