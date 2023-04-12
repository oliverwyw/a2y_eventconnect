import os
import sys
import math
import random
import numpy as np
from preprocess import preprocessText

# ----------------------- Class -----------------------
class VectorSpace:
    """
    VectorSpace class
    ------------------------
    ATTRIBUTE:
    ## Term Frequency Component
    tf - raw term frequency
    antf - augmented normalized term frequency
    max_tf - maximum term frequency in a document

    ## Collection Frequency Component
    N - number of documents
    df - document frequency
    idf - inverse document frequency
    pidf - probablistic inverse document frequency

    ## Weight
    wt - unnormailzed weights
    ------------------------
    STRUCTURE:
    tf, antf, wt:
    {word1: {doc1: data1, doc2: data2, doc3: data3},
     word2: {doc1: data1, doc3: data3},
     ...}

    max_tf:
    {doc1: data1,
     doc2: data2,
     ...}

    df, idf, pidf:
    {word1: data1,
     word2: data2,
     ...}

    N: int
    ------------------------
    ** Note: "word" and "term" are used interchangeably
    """


    def __init__(self):
        # Term Frequency Component
        self.tf = {}
        self.max_tf = {}
        self.antf = {}
        # Collection Frequency Component
        self.N = 0
        self.df = {}
        self.idf = {}
        self.pidf = {}
        # Weight
        self.wt = {}



    def _update_tf(self, doc_id: str, word_list: list):
        """
        helper function: update term frequency and max tf of a document

        param: doc_id - id of a document
        param: word_list - list of words in a document

        return: None
        """
        for word in word_list:
            # update tf
            if word not in self.tf:
                self.tf[word] = {}
                self.tf[word][doc_id] = 1
            else:
                if doc_id not in self.tf[word]:
                    self.tf[word][doc_id] = 1
                else:
                    self.tf[word][doc_id] += 1
            
            # update max_tf
            if doc_id not in self.max_tf:
                self.max_tf[doc_id] = 1
            else:
                if self.tf[word][doc_id] > self.max_tf[doc_id]:
                    self.max_tf[doc_id] = self.tf[word][doc_id]
        
        return
    
            

    def _update_df(self, word_list: list):
        """
        helper function: update document frequency of a document

        param: doc_id - id of a document
        param: word_list - list of words in a document

        return: None
        """

        counted_words = []
        for word in word_list:
            if word not in counted_words:
                if word not in self.df:
                    self.df[word] = 1
                else:
                    self.df[word] += 1
                counted_words.append(word)
        return



    def add_doc(self, doc_id: str, word_list: list):
        """
        add a document to the inverted index, update tf, df, and N

        param: doc_id - id of a document
        param: word_list - list of words in a document

        return: None
        """
        self._update_tf(doc_id, word_list)
        self._update_df(word_list)
        self.N += 1
        return
    


    def compute_doc_wt(self, doc_ws: str):
        """
        update document weights(wt) according to weighting scheme

        param: doc_ws - document weighting scheme

        return: None
        """
        # tfc
        if doc_ws == "tfc":
            # compute idf
            for word in self.df:
                self.idf[word] = math.log10(self.N / self.df[word])
            # compute tf-idf
            for word in self.tf:
                self.wt[word] = {}
                for doc_id in self.tf[word]:
                    self.wt[word][doc_id] = self.tf[word][doc_id] * self.idf[word]
        
        # npc
        elif doc_ws == "npc":
            # compute antf
            for word in self.tf:
                self.antf[word] = {}
                for doc_id in self.tf[word]:
                    self.antf[word][doc_id] = 0.5 + 0.5 * (self.tf[word][doc_id] / self.max_tf[doc_id])
            # compute pidf
            for word in self.df:
                self.pidf[word] = math.log10((self.N - self.df[word]) / self.df[word])
            # compute antf-pidf
            for word in self.tf:
                self.wt[word] = {}
                for doc_id in self.tf[word]:
                    self.wt[word][doc_id] = self.antf[word][doc_id] * self.pidf[word]



    def compute_query_wt(self, query_ws: str, N: int, doc_df: dict):
        """
        update query weights(wt) according to weighting scheme

        param: query_ws - query weighting scheme
        param: N - number of documents in the collection
        param: doc_df - document frequency of each word in the collection

        return: None
        """
        # tfx
        if query_ws == "tfx":
            # compute idf
            for word in self.df:
                if word not in doc_df:
                    doc_df[word] = 0
                self.idf[word] = math.log10(N / (doc_df[word] + 1))
            # compute tf-idf
            for word in self.df:
                self.wt[word] = {}
                self.wt[word]["query"] = self.tf[word]["query"] * self.idf[word]
        # tpx
        elif query_ws == "tpx":
            # compute pidf
            for word in self.df:
                if word not in doc_df:
                    doc_df[word] = 0
                self.pidf[word] = math.log10((N - doc_df[word]) / (doc_df[word] + 1))
            # compute tf-pidf
            for word in self.df:
                self.wt[word] = {}
                self.wt[word]["query"] = self.tf[word]["query"] * self.pidf[word]



    def sort_data(self):
        """
        sort data in the inverted index

        param: None

        return: None
        """
        # sort tf
        self.tf = dict(sorted(self.tf.items()))
        for word in self.tf:
            self.tf[word] = dict(sorted(self.tf[word].items()))

        # sort antf
        self.antf = dict(sorted(self.antf.items()))
        for word in self.antf:
            self.antf[word] = dict(sorted(self.antf[word].items()))

        # sort wt
        self.wt = dict(sorted(self.wt.items()))
        for word in self.wt:
            self.wt[word] = dict(sorted(self.wt[word].items()))

        # sort max_tf
        self.max_tf = dict(sorted(self.max_tf.items()))

        # sort df
        self.df = dict(sorted(self.df.items()))

        # sort idf
        self.idf = dict(sorted(self.idf.items()))

        # sort pidf
        self.pidf = dict(sorted(self.pidf.items()))



# ------------------------ Functions ------------------------
def indexDocument(doc_id: str, text: str, doc_ws: str, query_ws: str, inv_idx: VectorSpace):
    """
    add a document to the inverted index

    param: doc_id - id of a document
    param: text - text of a document
    param: doc_ws - weighting scheme for documents
    param: query_ws - weighting scheme for queries
    param: inv_idx - VectorSpace object

    return: inv_idx - VectorSpace object
    """
    # preprocess text
    word_list = preprocessText(text)
    inv_idx.add_doc(doc_id, word_list)
    return inv_idx



def retrieveDocuments(raw_query: str, inv_idx: VectorSpace, doc_ws: str, query_ws: str):
    """
    retrieve information from the index for a given query

    param: raw_query - query
    param: inv_idx - VectorSpace object
    param: doc_ws - weighting scheme for documents
    param: query_ws - weighting scheme for queries

    return: rel_docs - dict of relevant documents along with similarity scores
    """
    # process query
    query = preprocessText(raw_query)

    # find documents including query terms
    query_words = []
    docs = []
    for word in query:
        # add word to query_words
        if word not in query_words:
            query_words.append(word)
        # add doc to docs if they include "word", 
        if word in inv_idx.wt:
            for doc in inv_idx.wt[word]:
                if doc not in docs:
                    docs.append(doc)
    
    # sort query_words and docs
    query_words.sort()
    docs.sort()
    
    # create and fill in document weight matrix (unnormalized)
    wt_mtx = np.zeros((len(query_words), len(docs)))
    for i in range(len(query_words)):
        for j in range(len(docs)):
            if query_words[i] in inv_idx.wt and docs[j] in inv_idx.wt[query_words[i]]:
                wt_mtx[i, j] = inv_idx.wt[query_words[i]][docs[j]]
    
    # compute query weight
    query_inv_idx = VectorSpace()
    query_inv_idx.add_doc('query', query)
    query_inv_idx.compute_query_wt(query_ws, inv_idx.N, inv_idx.df)

    # get query weight
    query_wt = np.zeros(len(query_words))
    for i in range(len(query_words)):
        query_wt[i] = query_inv_idx.wt[query_words[i]]["query"]

    # compute cosine similarity
    rel_docs = {}
    for j in range(len(docs)):
        doc_vector = wt_mtx[:, j]
        normalized_doc_vector = doc_vector / np.linalg.norm(doc_vector)
        rel_docs[docs[j]] = np.dot(query_wt, normalized_doc_vector)
    
    # sort rel_docs
    rel_docs = dict(sorted(rel_docs.items(), key = lambda item: item[1], reverse = True))

    return rel_docs



def read_file(file):
    """
    Read a file and return text
    params: file - file object
    return: url - url of the event
            # title - event title
            # location - event location
            # time - event date & time
            # description - event description
            text - training text (Title + Description + Body Text (if exist))
    """
    content = file.readlines()
    # url = content[0].strip()
    # title = content[1].strip()
    # location = content[2].strip()
    # time = content[3].strip()
    # description = content[4].strip()
    text = content[5].strip()

    return text



def get_top_content(docs_sim, query_id):
    """
    Get info of top 10 relevant documents
    params: docs_sim - dict of relevant documents along with similarity scores
            query_id - id of the query
    return: title - event title
            location - event location
            time - event date & time
            description - event description
    """
    if len(docs_sim) < 10:
        top_10_file = list(docs_sim.keys())[0:len(docs_sim)]
    else:
        top_10_file = list(docs_sim.keys())[0:10]

    file_w = open(os.path.join("results/", "query_" + query_id + "_result.txt"), "w")
    for file in top_10_file:
        filename = file + ".txt"
        file = open(os.path.join('crawled_pages/', filename), 'r', encoding = 'iso-8859-1')
        content = file.readlines()
        url = content[0].strip()
        title = content[1].strip()
        location = content[2].strip()
        time = content[3].strip()
        description = content[4].strip()
        # write to file
        file_w.write(title + "\n")
        file_w.write("Location: " + location + "\n")
        file_w.write("Date & Time: " + time + "\n")
        file_w.write("URL: " + url + "\n")
        file_w.write("Description: " + description + "\n\n")
        file.close()
    file_w.close()




# ------------------------ Main ------------------------
if __name__ == "__main__":
    doc_ws = "tfc"
    query_ws = "tfx"
    doc_folder = "crawled_pages/"
    test_query_file = "test_queries.txt"

    # create inverted index
    inv_idx = VectorSpace()

    # index documents
    for filename in os.listdir(doc_folder):
        file = open(os.path.join(doc_folder, filename), 'r', encoding = 'iso-8859-1')
        # print(filename)
        text = read_file(file)
        file.close()
        doc_id = filename[:-4]
        inv_idx = indexDocument(doc_id, text, doc_ws, query_ws, inv_idx)

    # compute doc wt
    inv_idx.compute_doc_wt(doc_ws)

    # sort data
    inv_idx.sort_data()

    # read test queries
    file = open(test_query_file, 'r', encoding = 'iso-8859-1')
    queries = file.readlines()
    file.close()

    # retrieve documents
    for query in queries:
        query_lst = query.split()
        query_id = query_lst[0]
        query = ' '.join(query_lst[1:])
        docs_sim = retrieveDocuments(query, inv_idx, doc_ws, query_ws)
        # get top 10 relevant documents
        get_top_content(docs_sim, query_id)
        
    


