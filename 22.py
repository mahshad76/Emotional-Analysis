
import psycopg2
import nltk
from csv import reader
import numpy

con = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="mm123456"
)
cur = con.cursor()
cur.execute("select * from distinct_stemmed_pos")
positive = cur.fetchall()
cur.execute("select * from distinct_stemmed_neg")
negative = cur.fetchall()
sentences = []
for i in range(0, len(positive)):
    sentences.append(positive[i][0])

for i in range(0, len(negative)):
    sentences.append(negative[i][0])

with open(r'C:\Users\Mohammadreza Rahmani\Desktop\vocab_rbf.txt') as f:
    data = f.read()
vocab=eval(data)
with open(r'C:\Users\Mohammadreza Rahmani\Desktop\embed_result22.csv', 'r') as read_obj:
    csv_reader = reader(read_obj)
    list_of_rows = list(csv_reader)
train_data = numpy.array(list_of_rows)
train = []
for item in train_data:
    b = numpy.asarray(item, dtype=numpy.float64, order='C')
    train.append(list(b))
res=[]
for i in range(0,2000):
    list=[0]*100
    nltk_tokens = nltk.word_tokenize(sentences[i])
    for token in nltk_tokens:
        index=-1
        for j in range(0,len(vocab)):
            if token==vocab[j]:
                index=j
                break
        if index!=-1:
            zipped_lists = zip(list, train[index])
            list = [x + y for (x, y) in zipped_lists]
    res.append(list)


for i in range(99999,102000):
    list=[0]*100
    nltk_tokens = nltk.word_tokenize(sentences[i])
    for token in nltk_tokens:
        index=-1
        for j in range(0,len(vocab)):
            if token==vocab[j]:
                index=j
                break
        if index!=-1:
            zipped_lists = zip(list, train[index])
            list = [x + y for (x, y) in zipped_lists]
    res.append(list)
import csv
with open(r"C:\Users\Mohammadreza Rahmani\Desktop\embedding_train.csv", "w", newline="") as f:
	writer = csv.writer(f)
	writer.writerows(res)

