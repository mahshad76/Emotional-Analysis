#IDF = Log((Total number of docs)/(Number of docs containing the word))
import psycopg2
from nltk.tokenize import word_tokenize
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import math

con=psycopg2.connect(
     host="localhost",
     database="postgres",
     user="postgres",
    password="mm123456"
 )
cur=con.cursor()

stop_words = set(stopwords.words('english'))
cur.execute("select * from stemmed_positive")
positive=cur.fetchall()
cur.execute("select * from stemmed_negative")
negative=cur.fetchall()
negative=negative[0:2000]
positive=positive[0:2000]
total_word=0
for i in range(0,len(negative)):
    tokens = word_tokenize(negative[i][0])
    total_word+=len(tokens)
for i in range(0,len(positive)):
    tokens = word_tokenize(positive[i][0])
    total_word+=len(tokens)
print(total_word)
with open(r'C:\Users\Mohammadreza Rahmani\Desktop\tweet_count.txt') as f:
    data = f.read()
tweetcount = eval(data)
vocab=list(tweetcount.keys())
#print(vocab)
#for i in range(0,len(vocab)):
   # cur.execute(("insert into vocabulary(txt) values('%s')")%(vocab[i]))
#for i in range(0,len(vocab)):
 #   idf=math.log((total_word/tweetcount.get(vocab[i])),10)
        #((len(positive)+len(negative))(100000+100000)/tweetcount.get(vocab[i])),10)
  #  cur.execute(("insert into idf(num) values(%s)")%(idf))
   # con.commit()
    #print(3)
