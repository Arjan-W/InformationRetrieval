import math
import numpy as np
import heapq

class RM3:

    def query_lang_model(self, termid, query):
        term = self.get_term(termid)
        count = 0
        for qterm in query:
            if term == qterm:
                count += 1
        return count


    def doc_term_count(self, termid, docid):
        query = "SELECT count FROM terms WHERE termid = {} AND docid = {}".format(termid, docid)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result:
            count = result[0]
        else:
            count = 0
        return count

    def doc_lang_model(self, termid, docid, doc_length, collection_ids):
        doc_count = self.doc_term_count(termid, docid)
        collection_count = self.get_collection_count(termid, collection_ids)
        val = (1 - self.smoothing) * (doc_count / doc_length) + self.smoothing * (collection_count / self.collection_length)
        return val

    def get_collection_count(self, termid, collection_ids):
        collection_ids_string = self.convert_collection_ids(collection_ids)
        query = "SELECT count FROM terms WHERE termid = {} AND docid IN ({})".format(termid, collection_ids_string
                                                                                     )
        self.cursor.execute(query)
        count = np.sum(self.cursor.fetchnumpy()['count'])
        return count

    def convert_collection_ids(self, collection_ids):
        collection_ids_string = ""
        for i in range(len(collection_ids)):
            collection_ids_string += str(collection_ids[i])
            if i < len(collection_ids) - 1:
                collection_ids_string += ", "
        return collection_ids_string

    def get_term(self, term_id):
        query = "SELECT term FROM dict WHERE termid = {}".format(term_id)
        self.cursor.execute(query)
        term = self.cursor.fetchone()[0]
        return term

    def rm3(self):
        ranking = self.ranking
        k = self.k
        # Get all terms present in the collection
        amount_of_docs = len(ranking['doc_id'])
        col_ids = ranking['doc_id']
        col_ids_string = self.convert_collection_ids(col_ids)
        sql_query = "SELECT DISTINCT termid FROM TERMS WHERE docid IN ({})".format(col_ids_string)
        self.cursor.execute(sql_query)
        terms = self.cursor.fetchnumpy()
        amount_of_terms = len(terms['termid'])

        term_probs = []

        for i in range(amount_of_terms):
            term_id = terms['termid'][i]
            term_prob = 0
            qlm = self.query_lang_model(term_id, self.query)
            for i in range(amount_of_docs):
                doc_id = ranking['doc_id'][i]
                doc_len = ranking['length'][i]
                doc_prob = ranking['prob'][i]

                word_doc_model = self.doc_lang_model(term_id, doc_id, doc_len, col_ids)
                term_prob += word_doc_model * doc_prob
            p_rm3 = self.alpha * qlm + (1 - self.alpha) * term_prob
            term_probs.append(p_rm3)

        # Get indices of N largest terms
        largest_probs_indices = heapq.nlargest(k, range(len(term_probs)), term_probs.__getitem__)
        term_ids = []
        # Print selected terms
        for i in range(k):
            index = largest_probs_indices[i]
            term_ids.append(terms['termid'][index])
            #term = self.get_term(term_id)
            #print(str(i) + " " + term + " " + str(term_probs[index]))

        return self.convert_collection_ids(term_ids)

    # k = number of terms to select
    # smoothing = smoothing parameter (Jellinek-Mercer)
    # alpha = linear interpolation parameter query language model and RM1
    def __init__(self, cursor, query, ranking, smoothing, alpha, k):
        self.cursor = cursor
        self.query = query
        self.ranking = ranking
        self.collection_length = len(ranking)
        self.smoothing = smoothing
        self.alpha = alpha
        self.k = k

