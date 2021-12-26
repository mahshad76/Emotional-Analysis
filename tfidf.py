import psycopg2
from nltk.tokenize import word_tokenize
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

con=psycopg2.connect(
     host="localhost",
     database="postgres",
     user="postgres",
    password="mm123456"
 )
cur=con.cursor()
cur.execute("select * from stemmed_positive")
positive=cur.fetchall()
cur.execute("select * from stemmed_negative")
negative=cur.fetchall()
cur.execute("select * from idf")
idf=cur.fetchall()
negative=negative[0:2000]
positive=positive[0:2000]
with open(r'C:\Users\Mohammadreza Rahmani\Desktop\tweet_count.txt') as f:
    data = f.read()
tweetcount = eval(data)
vocab=list(tweetcount.keys())
for i in range(0,len(positive)):
    tokens = word_tokenize(positive[i][0])
    freq=len(tokens)
    tfidf = []
    indexes=[]
    mini_dict={}
    listi=[]
    for eleman in tokens:
        if(eleman in mini_dict.keys()):
            mini_dict.update({eleman:mini_dict.get(eleman)+1})
        else:
            mini_dict.update({eleman:1})
    for key in list(mini_dict.keys()):
        indexes.append(vocab.index(key))
        tf=(mini_dict.get(key))/sum(list(mini_dict.values()))
        tfidf.append(idf[vocab.index(key)][0]*tf)
    listi.append(tfidf)
    listi.append(indexes)
    cur.execute(("insert into tf_idf_pos(str) values('%s')")%(listi))
    con.commit()
    print(1)
for i in range(0,len(negative)):
    tokens = word_tokenize(negative[i][0])
    freq=len(tokens)
    tfidf = []
    indexes=[]
    listi=[]
    mini_dict={}
    for eleman in tokens:
        if(eleman in mini_dict.keys()):
            mini_dict.update({eleman:mini_dict.get(eleman)+1})
        else:
            mini_dict.update({eleman:1})
    for key in list(mini_dict.keys()):
        indexes.append(vocab.index(key))
        tf=(mini_dict.get(key))/sum(list(mini_dict.values()))
        tfidf.append(idf[vocab.index(key)][0]*tf)
    listi.append(tfidf)
    listi.append(indexes)
    cur.execute(("insert into tf_idf_neg(str) values('%s')")%(listi))
    con.commit()
    print(2)
