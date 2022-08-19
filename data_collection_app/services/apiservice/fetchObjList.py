# from nltk.corpus import words as words

# # from nltk.wsd import lesk
# # from nltk.tokenize import word_tokenize
# def getWords(keyword):
#     for w in wn.synsets(keyword):
#         return w.name();
from elasticsearch import Elasticsearch
import re
import os


def esearch(q=""):    
    print(q)
    q = re.sub('[^a-zA-Z]+', '', q)
    client = Elasticsearch('http://elasticsearch:9200', http_auth=('elastic', 'welcome'), verify_certs=False)

    query = {
        "query": {
            "query_string": {
            "query": "*"+str(q)+"*",
            "fields": ["word", "definition"]
        }}}
    # print(query)
    response = client.search(index="test-index", body=query, size=5)
    # es.indices.refresh(index="test-index")

    # print("Got %d Hits:" % response['hits']['total']['value'])
    search = get_results(response)    
    return search

def get_results(response): 
    results = []  
    for hit in response['hits']['hits']:
        result_dict = {}
        result_dict['word'] = hit['_source']['word']
        result_dict['definition'] = hit['_source']['definition']
        results.append(result_dict)  
    return results