import math
import numpy as np

class RM3:


    # def doc_lang_model(self, doc_count, doc_length, collection_count, collection_length, param):
    #     return (1 - param) * (doc_count / doc_length) + param * (collection_count / collection_length)

    def doc_term_count(self, termid, docid):
        query = "SELECT count FROM terms WHERE termid = {} AND docid = {}".format(termid, docid)
        self.cursor.execute(query)
        count = self.cursor.fetchone()[0]
        return count

    # def doc_lang_model(self, termid, docid, collection_ids):
    #     val = 0
    #     val += (1 - self.smoothing) * doc_term_count(termid, docid) /

    def get_collection_count(self, termid, collection_ids):
        query = "SELECT count FROM terms WHERE termid = {} AND docid IN ({})".format(termid, collection_ids)
        self.cursor.execute(query)
        count = np.sum(self.cursor.fetchnumpy()['count'])
        return count

    def convert_collection_ids(self, collection_ids):
        collection_ids_string = ""
        for i in range(self.collection_length):
            collection_ids_string += str(collection_ids[i])
            if i < self.collection_length - 1:
                collection_ids_string += ", "
        return collection_ids_string

    def rm3(self, ranking):
        # Get all terms present in the collection
        doc_ids = ranking['doc_id']
        col_ids = self.convert_collection_ids(ranking['doc_id'])
        sql_query = "SELECT DISTINCT termid FROM TERMS WHERE docid IN ({})".format(col_ids)
        self.cursor.execute(sql_query)
        terms = self.cursor.fetchnumpy()
        amount_of_terms = len(terms['termid'])

        for doc_id in doc_ids:





    def __init__(self, cursor, ranking, smoothing):
        self.cursor = cursor
        self.ranking = ranking
        self.collection_length = len(ranking)
        self.smoothing = smoothing
        self.rm3(ranking)