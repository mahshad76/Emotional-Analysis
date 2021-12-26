import json
import psycopg2
con=psycopg2.connect(
     host="localhost",
     database="postgres",
     user="postgres",
    password="mm123456"
 )
cur=con.cursor()

with open(r'C:\Users\Mohammadreza Rahmani\Desktop\naive bayes\geekyfile1.txt') as f:
    data = f.read()
positive_dict = eval(data)
with open(r'C:\Users\Mohammadreza Rahmani\Desktop\naive bayes\geekyfile2.txt') as f:
    data = f.read()
negative_dict = eval(data)
with open(r'C:\Users\Mohammadreza Rahmani\Desktop\tweet_count.txt') as f:
    data = f.read()
tweetcount = eval(data)
result=list(tweetcount.keys())
for i in range(0,len(result)):
    pos_count=positive_dict.get(result[i])
    print(pos_count)
    if(pos_count is None):
        pos_count=0
    neg_count=negative_dict.get(result[i])
    print(neg_count)
    if(neg_count is None):
        neg_count=0
    pos_prob=(pos_count+1)/(sum(positive_dict.values())+len(result))
    neg_prob = (neg_count + 1) / (sum(negative_dict.values()) + len(result))
    query="insert into probabilities values(%s,%s)"%(pos_prob,neg_prob)
    cur.execute(query)
    con.commit()
    print(1)