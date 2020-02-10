
## Creates index for future queries
## Salvador Gutierrez 
## 03/08/2019 @ 3:52 p.m


import nltk
import json
import pickle
from math import log
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
# nltk.download('punkt')
from bs4 import BeautifulSoup, Comment
from collections import defaultdict
import re
import os
from sys import getsizeof

dict_index = defaultdict(dict)

_JPATH = "WEBPAGES_RAW/bookkeeping.json"
# _JPATH2 = "TEST/bookkeeping.json"
_DOCS = 0
stop_words = set(stopwords.words('english'))
_UNIQUE_WORDS = set()



def query(db,input):

    result = []
    ranked = dict()
    global _JPATH

    with open(_JPATH) as file:
        obj = json.load(file)

        for token in input:
            docs = db[token.lower()]
            for doc_id, rank in docs.items():  ##{token: {doc_id,tf-idf}}
                if doc_id in ranked:
                    ranked[doc_id] = rank *1.5 ## if the doc_id appears again increase the rank
                else: ## else not in ranked dict already so just add it
                    ranked[doc_id] = rank


        ## after we populate new ranked dictionary get resulting urls sorted by rank
        for doc_id, rank in sorted(ranked.items(), key = lambda x: x[1], reverse =True): 
            # print doc_id, rank
            result.append(obj[doc_id]) ## add url

    return result




## parse document passed in
def parse_doc(document):
    with open(document) as f:
        try:
            soup = BeautifulSoup(f.read(), 'lxml') ## parse page
            clean_soup(soup) ## clean html
        except ParseError:
            print("COULD NOT PARSE!!")
    return soup        

        

def tokenize_data(data):
    
    ## format-> {token: [(doc_id,tf-idf)]}
    t = re.findall(r'[a-zA-Z]{3,}',data) ## excludes numbers
    return t

    

def initialize_index():
    global _DOCS
    _PATH = "./WEBPAGES_RAW"

    _IDF = 0
    # _PATH = "TEST"
    index = defaultdict(dict)
    result = defaultdict()
    global stop_words
    for subdir, dirs, files in os.walk(_PATH):
        
        for file in files:
            ## I only want the html documents
            if not file.endswith('.json') and not file.endswith('.tsv') and '.DS_Store' not in file:
                doc_path = os.path.join(subdir,file) ## create path to open file
                _DOCS += 1
                # id = doc_path.replace("./TEST","") ## get doc_id
                id = doc_path.replace("./WEBPAGES_RAW/","") ## get doc_id

                html_text = parse_doc(doc_path)

                extract_tag(index,html_text,id,"body")
                extract_tag(index,html_text,id,"title")
                extract_tag(index,html_text,id,"strong")
                extract_tag(index,html_text,id,"p")
                extract_tag(index,html_text,id,"h1")

    ## update index values to TF_IDF
    for docs in index.values():
        _IDF = log(float(_DOCS)/len(docs))
        for k,tf in docs.items():
            docs[k] = _IDF * tf
    return index

def extract_tag(index,html_text, doc_id, tag):

    _frequency = 0 
    extracted = defaultdict(int)
    for t in html_text.find_all(tag):
        data = t.text
        all_tokens = tokenize_data(data.lower())
        for token in all_tokens:
            if token not in stop_words: ## ignore stop_words
                extracted[token]+=1 ## {token:term_frequency}

        for key, tf in extracted.items():
            _frequency = 1+log(float(tf))

            index[key].update({doc_id:_frequency}) ## format -> {"token":{doc1:tf}}

def create_pickle(index):
    with open('index.pickle','wb') as pick:
        pickle.dump(index, pick, protocol=pickle.HIGHEST_PROTOCOL)

def output():
    global _DOCS
    global _UNIQUE_WORDS
    global dict_index
    with open("index_db.txt", "w") as file:
        file.write("\nNumber of Documents: {}\n".format(_DOCS) )
        file.write("\nTotal Unique Words: {}\n".format(len(_UNIQUE_WORDS)))
        KB = getsizeof(dict_index)/1000
        file.write("\nSize of Index {} KB\n".format(KB))

def load_pickle(p):
    with open(p, 'rb') as pick:
        data = pickle.load(pick)
        return data

def clean_soup(soup):
    [s.extract() for s in soup.find_all('script')] ## remove script from html
    [s.extract() for s in soup.find_all('style')]
    [s.extract() for s in soup.find_all('meta')] ## remove meta data
    [s.extract() for s in soup.find_all(text = lambda text:isinstance(text, Comment))] ## remove html comments
    
    return soup ## return cleaned html



