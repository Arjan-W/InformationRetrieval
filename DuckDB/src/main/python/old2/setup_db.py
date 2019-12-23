import duckdb

folder = "C:\\"

create_docs = """ CREATE TABLE docs (
    collection_id   VARCHAR,
    id              INTEGER,
    len             INTEGER, 
    irr             INTEGER 
);
"""

create_dict = """ CREATE TABLE dict (
    termid          INTEGER,
    term            VARCHAR, 
    df              INTEGER 
);
"""

create_terms = """CREATE TABLE terms (
    termid          INTEGER,
    docid           INTEGER,
    count           INTEGER
);
"""

copy_docs = """ COPY docs
FROM '{}docs.csv' 
WITH (DELIMITER '|')
"""

copy_dict = """ COPY dict
FROM '{}dict.csv' 
WITH (DELIMITER '|')
"""

copy_terms = """ COPY terms
FROM '{}terms.csv' 
WITH (DELIMITER '|')
"""

create_index_terms = """
CREATE INDEX termid_index
ON terms (termid);
"""

create_index_docs = """
CREATE INDEX docid_index
ON docs (id);
"""

create_index_dict = """
CREATE INDEX termid_dict_index
ON dict (termid);
"""

def setup(cursor):
    cursor.execute(create_dict)
    cursor.execute(create_docs)
    cursor.execute(create_terms)
    cursor.execute(copy_docs.format(folder))
    cursor.execute(copy_dict.format(folder))
    cursor.execute(copy_terms.format(folder))
    cursor.execute(create_index_terms)
    cursor.execute(create_index_docs)
    cursor.execute(create_index_dict)





