import psycopg2
from nltk.tokenize import word_tokenize
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import json
import math

con=psycopg2.connect(
     host="localhost",
     database="postgres",
     user="postgres",
    password="mm123456"
 )
cur=con.cursor()

def combine(pos_dist,neg_dist):
    dists=pos_dist+neg_dist
    dists = sorted(dists)
    dists = [ele for ele in reversed(dists)]
    count_pos=0
    count_neg=0
    dists=dists[0:500]
    for item in dists:
        if item in pos_dist:
            pos_dist.remove(item)
            count_pos+=1
        elif item in neg_dist:
            neg_dist.remove(item)
            count_neg+=1
    return count_pos,count_neg

stop_words = set(stopwords.words('english'))
cur.execute("select * from tf_idf_neg")
tfidf_neg=cur.fetchall()
cur.execute("select * from tf_idf_pos")
tfidf_pos=cur.fetchall()
cur.execute("select * from pos_distinct")
positive=cur.fetchall()
cur.execute("select * from neg_distinct")
negative=cur.fetchall()
cur.execute("select * from vocabulary")
vocab=cur.fetchall()
cur.execute("select * from idf")
idf=cur.fetchall()
negative=negative[198000:200000]
positive=positive[198000:200000]
similarity_pos=[]
similarity_neg=[]
for i in range(0,len(positive)):
    pattern = r'[0-9]'
    data = re.sub(pattern, ' ', positive[i][0])
    pattern=r"['™', '©', '®', '‰', '±', '¼', '½', '¾', '≡', '≈', '≥', '≤', '√', 'ⁿ', '¹', '²', '³', 'π', '°', '∞', 'µ', 'Σ', '☺', '☻', '•', '○', '♂', '♀', '↨', '↑', '↓', '→', '←', '↔', '£', '€', '$', '¢', '¥', 'ƒ', '₧', 'α', 'ß', 'δ', 'Ω', '►', '◄', '■', '▲', '▼', '§', '¶', '“', '”', '«', '»', '♥', 'º', 'œ', '•', '↻', '↺', 'Ø', 'Ñ', 'Ø', '±', 'Ù', '†', '§', '…', '‡', '¬', 'Û', 'Œ', 'Ú', '©', '´', '¾', '„', 'ª', 'µ', '¯', 'Ø³', 'Ø¹', 'ˆ', '®', 'Ø²', 'Ø°', 'º', 'â', '€', 'Ž']"
    data = re.sub(pattern, ' ', data)
    tokens = word_tokenize(data)
    ps = PorterStemmer()
    stemmed_words = [ps.stem(w) for w in tokens]
    stemmed_words = [w for w in stemmed_words if not w in stop_words]
    freq = len(stemmed_words)
    tfidf = []
    indexes = []
    mini_dict = {}
    for eleman in stemmed_words:
        if(eleman in mini_dict.keys()):
            mini_dict.update({eleman:mini_dict.get(eleman)+1})
        else:
            mini_dict.update({eleman:1})
    for key in list(mini_dict.keys()):
        if((key,) in vocab):
            indexes.append(vocab.index((key,)))
            m=0
            for ii in range(0,len(list(mini_dict.values()))):
                m+=(list(mini_dict.values()))[ii]
            tf=(mini_dict.get(key))/m
            tfidf.append(idf[vocab.index((key,))][0]*tf)
        else:
            m = 0
            for ii in range(0, len(list(mini_dict.values()))):
                m += (list(mini_dict.values()))[ii]
            tf = (mini_dict.get(key)) / m
            tfidf.append(math.log(31046, 10) * tf)
    for j in range(0,len(tfidf_pos)):
        sum=0.0
        res = json.loads(tfidf_pos[j][0])
        res_tfidf=res[0]
        res_indexes=res[1]
        intersect_index=list(set(indexes) & set(res_indexes))
        if(len(intersect_index)!=0):
            for j2 in range(0,len(intersect_index)):
                sum+=tfidf[indexes.index(intersect_index[j2])]*res_tfidf[res_indexes.index(intersect_index[j2])]
        len1=0
        len2=0
        for j2 in range(0,len(tfidf)):
            len1+=tfidf[j2]*tfidf[j2]
        len1=math.sqrt(len1)

        for j2 in range(0,len(res_tfidf)):
            len2+=res_tfidf[j2]*res_tfidf[j2]
        len2=math.sqrt(len2)
        similar=sum/(len1*len2)
        similarity_pos.append(similar)
    similarity_pos=sorted(similarity_pos)
    similarity_pos=[ele for ele in reversed(similarity_pos)]
    similarity_pos=similarity_pos[0:1000]


    for j in range(0,len(tfidf_neg)):
        sum=0.0
        res = json.loads(tfidf_neg[j][0])
        res_tfidf=res[0]
        res_indexes=res[1]
        intersect_index=list(set(indexes) & set(res_indexes))
        if(len(intersect_index)!=0):
            for j2 in range(0,len(intersect_index)):
                sum+=tfidf[indexes.index(intersect_index[j2])]*res_tfidf[res_indexes.index(intersect_index[j2])]
        len1=0
        len2=0
        for j2 in range(0,len(tfidf)):
            len1+=tfidf[j2]*tfidf[j2]
        len1=math.sqrt(len1)

        for j2 in range(0,len(res_tfidf)):
            len2+=res_tfidf[j2]*res_tfidf[j2]
        len2=math.sqrt(len2)
        similar=sum/(len1*len2)
        similarity_neg.append(similar)
    similarity_neg=sorted(similarity_neg)
    similarity_neg=[ele for ele in reversed(similarity_neg)]
    similarity_neg=similarity_neg[0:1000]
    result=combine(similarity_pos,similarity_neg)
    print(result)
    if(result[0]>result[1]):
        cur.execute("insert into knn_pos values('positive')")
        con.commit()
    elif(result[0]==result[1]):
        cur.execute("insert into knn_pos values('neutral')")
        con.commit()
    else:
        cur.execute("insert into knn_pos values('negative')")
        con.commit()
    print(1)

similarity_pos=[]
similarity_neg=[]
for i in range(0,len(negative)):
    pattern = r'[0-9]'
    data = re.sub(pattern, ' ', negative[i][0])
    pattern=r"['™', '©', '®', '‰', '±', '¼', '½', '¾', '≡', '≈', '≥', '≤', '√', 'ⁿ', '¹', '²', '³', 'π', '°', '∞', 'µ', 'Σ', '☺', '☻', '•', '○', '♂', '♀', '↨', '↑', '↓', '→', '←', '↔', '£', '€', '$', '¢', '¥', 'ƒ', '₧', 'α', 'ß', 'δ', 'Ω', '►', '◄', '■', '▲', '▼', '§', '¶', '“', '”', '«', '»', '♥', 'º', 'œ', '•', '↻', '↺', 'Ø', 'Ñ', 'Ø', '±', 'Ù', '†', '§', '…', '‡', '¬', 'Û', 'Œ', 'Ú', '©', '´', '¾', '„', 'ª', 'µ', '¯', 'Ø³', 'Ø¹', 'ˆ', '®', 'Ø²', 'Ø°', 'º', 'â', '€', 'Ž']"
    data = re.sub(pattern, ' ', data)
    tokens = word_tokenize(data)
    ps = PorterStemmer()
    stemmed_words = [ps.stem(w) for w in tokens]
    stemmed_words = [w for w in stemmed_words if not w in stop_words]
    freq = len(stemmed_words)
    tfidf = []
    indexes = []
    mini_dict = {}
    for eleman in stemmed_words:
        if(eleman in mini_dict.keys()):
            mini_dict.update({eleman:mini_dict.get(eleman)+1})
        else:
            mini_dict.update({eleman:1})
    for key in list(mini_dict.keys()):
        if((key,) in vocab):
            indexes.append(vocab.index((key,)))
            m=0
            for ii in range(0,len(list(mini_dict.values()))):
                m+=(list(mini_dict.values()))[ii]
            tf=(mini_dict.get(key))/m
            tfidf.append(idf[vocab.index((key,))][0]*tf)
        else:
            m = 0
            for ii in range(0, len(list(mini_dict.values()))):
                m += (list(mini_dict.values()))[ii]
            tf = (mini_dict.get(key)) / m
            tfidf.append(math.log(31046, 10) * tf)
    for j in range(0,len(tfidf_pos)):
        sum=0.0
        res = json.loads(tfidf_pos[j][0])
        res_tfidf=res[0]
        res_indexes=res[1]
        intersect_index=list(set(indexes) & set(res_indexes))
        if(len(intersect_index)!=0):
            for j2 in range(0,len(intersect_index)):
                sum+=tfidf[indexes.index(intersect_index[j2])]*res_tfidf[res_indexes.index(intersect_index[j2])]
        len1=0
        len2=0
        for j2 in range(0,len(tfidf)):
            len1+=tfidf[j2]*tfidf[j2]
        len1=math.sqrt(len1)

        for j2 in range(0,len(res_tfidf)):
            len2+=res_tfidf[j2]*res_tfidf[j2]
        len2=math.sqrt(len2)
        similar=sum/(len1*len2)
        similarity_pos.append(similar)
    similarity_pos=sorted(similarity_pos)
    similarity_pos=[ele for ele in reversed(similarity_pos)]
    similarity_pos=similarity_pos[0:1000]


    for j in range(0,len(tfidf_neg)):
        sum=0.0
        res = json.loads(tfidf_neg[j][0])
        res_tfidf=res[0]
        res_indexes=res[1]
        intersect_index=list(set(indexes) & set(res_indexes))
        if(len(intersect_index)!=0):
            for j2 in range(0,len(intersect_index)):
                sum+=tfidf[indexes.index(intersect_index[j2])]*res_tfidf[res_indexes.index(intersect_index[j2])]
        len1=0
        len2=0
        for j2 in range(0,len(tfidf)):
            len1+=tfidf[j2]*tfidf[j2]
        len1=math.sqrt(len1)

        for j2 in range(0,len(res_tfidf)):
            len2+=res_tfidf[j2]*res_tfidf[j2]
        len2=math.sqrt(len2)
        similar=sum/(len1*len2)
        similarity_neg.append(similar)
    similarity_neg=sorted(similarity_neg)
    similarity_neg=[ele for ele in reversed(similarity_neg)]
    similarity_neg=similarity_neg[0:1000]
    result=combine(similarity_pos,similarity_neg)
    print(result)
    if(result[0]>result[1]):
        cur.execute("insert into knn_neg values('positive')")
        con.commit()
    elif(result[0]==result[1]):
        cur.execute("insert into knn_neg values('neutral')")
        con.commit()
    else:
        cur.execute("insert into knn_neg values('negative')")
        con.commit()
    print(1)


