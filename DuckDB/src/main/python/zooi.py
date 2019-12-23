def querytest_single(self):
    ofile = open(self.args.output, 'w+')
    topics = self.topicReader.get_topics()
    self.cursor.execute("SELECT COUNT(*) FROM docs WHERE len > 0;")
    collection_size = self.cursor.fetchone()[0]

    self.cursor.execute("SELECT AVG(len) FROM docs WHERE len > 0;")
    avg_doc_len = self.cursor.fetchone()[0]

    topic = topics[0]

    query_terms = topic['title'].split(" ")
    ids = []  # Term ids
    for qterm in query_terms:
        self.cursor.execute("SELECT termid FROM dict WHERE dict.term = '{}'".format(qterm))
        term_id = self.cursor.fetchone()
        if term_id:
            ids.append(str(term_id[0]))
    term_ids = ", ".join(ids)
    if self.args.disjunctive:
        sql_query = self.getQueryTemplate(collection_size, avg_doc_len).format(term_ids)
    else:
        sql_query = self.getQueryTemplate(collection_size, avg_doc_len).format(term_ids, len(ids))
    if self.args.time:
        sql_query = 'TRACE ' + sql_query

    self.cursor.execute(sql_query)

    output = self.cursor.fetchall()
    dup = 0
    last_score = 0
    collection_ids = []  # Collection ids
    for rank, row in enumerate(output):
        collection_id, score = row
        collection_ids.append(collection_id)
        if self.args.breakTies:
            score = round(score * 10 ** 4) / 10 ** 4
            if rank == 0 or (last_score - score) > 10 ** (-4):
                dup = 0
            else:
                dup += 1
                score -= 10 ** (-6) * dup
            last_score = score
        ofile.write(
            "{} Q0 {} {} {:.6f} olddog\n".format(topic['number'], collection_id, rank + 1, score))
        ofile.close()


def rm3(self, query_terms, collection_ids):
    # Query likelihood
    ids = []
    collection_length = len(collection_ids)
    unique_terms = []
    for qterm in query_terms:
        self.cursor.execute("SELECT termid FROM dict WHERE dict.term = '{}'".format(qterm))
        term_id = self.cursor.fetchone()
        if term_id:
            ids.append(str(term_id[0]))

        # Get p(w|theta_d)


def testdb(self):
    termid = 841673
    document_id = 579761
    doc_query = get_doc_count(termid, document_id)
    self.cursor.execute(doc_query)
    doc_count = self.cursor.fetchone()[0]
    print(doc_count)

    termid = 841674
    collection_ids = ['582578', '582584']

    col_query = get_collection_count(termid, collection_ids)
    self.cursor.execute(col_query)
    col_counts = self.cursor.fetchnumpy()
    print(col_counts['count'])
    print(np.sum(col_counts['count']))

    document_id = 595033
    doc_length_query = get_doc_length(document_id)
    self.cursor.execute(doc_length_query)
    doc_length = self.cursor.fetchone()[0]
    print(doc_length)

    ##  Calculate p(q|theta_d)
    ##  termid : int
    ##  document_id : int
    ##  collection_ids: [] of strings with collection ids
    ##  param : float in (0, 1)

    ##  Calculate p(w|theta_d)
    ##  termid : int
    ##  document_id : int
    ##  collection_ids: [] of strings with collection ids
    ##  param : float in (0, 1)


def dlm_single_word(self, termid, document_id, collection_ids, param):
    col_length = len(collection_ids)

    doc_query = get_doc_count(termid, document_id)
    self.cursor.execute(doc_query)
    doc_count = self.cursor.fetchone()[0]

    col_query = get_collection_count(termid, collection_ids)
    self.cursor.execute(col_query)
    col_count = np.sum(self.cursor.fetchnumpy()['count'])

    doc_length_query = get_doc_length(document_id)
    self.cursor.execute(doc_length_query)
    doc_length = self.cursor.fetchone()[0]

    return math.log(((1 - param) * doc_count / doc_length) + (param * col_count / col_length))


def dlm_query(self, termids, document_id, collection_ids, param):
    total = 0
    for termid in termids:
        total += self.dlm_single_word(termid, document_id, collection_ids, param)
