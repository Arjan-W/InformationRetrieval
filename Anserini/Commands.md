# Running Anserini

## Installing maven

apt-get install maven -qq

## Installing and building Anserini with Maven

git clone https://github.com/castorini/anserini.git
cd anserini
mvn clean package appassembler:assemble -DskipTests -Dmaven.javadoc.skip=true

## Obtaining the correct data

cd eval && tar xvfz trec_eval.9.0.4.tar.gz && cd trec_eval.9.0.4 && make
wget https://www.dropbox.com/s/6898ioi0cod8cjk/lucene-index.core18.pos%2Bdocvectors%2Brawdocs.zip
unzip lucene-index.core18.pos+docvectors+rawdocs.zip
du -h lucene-index.core18.pos+docvectors+rawdocs

## Running BM25/RM3

target/appassembler/bin/SearchCollection -index eval/trec_eval/lucene-index.core18.pos+docvectors+rawdocs \
-topicreader Trec -topics src/main/resources/topics-and-qrels/topics.core18.txt \
-bm25 -output run.core18.bm25.topics.core18.txt &

For RM3 add "-rm3" after "-bm25" on the third line

## Obtain scores

eval/trec_eval.9.0.4/trec_eval -c src/main/resources/topics-and-qrels/qrels.core18.txt run.core18.bm25.topics.core18.txt