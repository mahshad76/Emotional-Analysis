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

stop_words = set(stopwords.words('english'))
cur.execute("select * from pos_distinct")
positive=cur.fetchall()
cur.execute("select * from neg_distinct")
negative=cur.fetchall()
negative=negative[0:2000]
positive=positive[0:2000]
vocab_neg={}
vocab_pos={}
tweet_count={}

for i in range(0,len(positive)):
    pattern = r'[0-9]'
    data = re.sub(pattern, ' ', positive[i][0])
    pattern=r"['™', '©', '®', '‰', '±', '¼', '½', '¾', '≡', '≈', '≥', '≤', '√', 'ⁿ', '¹', '²', '³', 'π', '°', '∞', 'µ', 'Σ', '☺', '☻', '•', '○', '♂', '♀', '↨', '↑', '↓', '→', '←', '↔', '£', '€', '$', '¢', '¥', 'ƒ', '₧', 'α', 'ß', 'δ', 'Ω', '►', '◄', '■', '▲', '▼', '§', '¶', '“', '”', '«', '»', '♥', 'º', 'œ', '•', '↻', '↺', 'Ø', 'Ñ', 'Ø', '±', 'Ù', '†', '§', '…', '‡', '¬', 'Û', 'Œ', 'Ú', '©', '´', '¾', '„', 'ª', 'µ', '¯', 'Ø³', 'Ø¹', 'ˆ', '®', 'Ø²', 'Ø°', 'º', 'â', '€', 'Ž','Ã','¯','Â','¿','ø','Ã','£']"
    data = re.sub(pattern, ' ', data)
    tokens = word_tokenize(data)
    ps = PorterStemmer()
    stemmed_words = [ps.stem(w) for w in tokens]
    stemmed_words = [w for w in stemmed_words if not w in stop_words]
    for item in stemmed_words:
        if item in vocab_pos.keys():
            vocab_pos.update({item:vocab_pos.get(item)+1})
        else:
            vocab_pos.update({item:1})
    tweet = " ".join(stemmed_words)
    cur.execute(("insert into stemmed_positive(txt) values('%s')")%(tweet))
    con.commit()
    stemmed_words=list(set(stemmed_words))
    for item in stemmed_words:
        if(item in tweet_count.keys()):
            tweet_count.update({item:tweet_count.get(item)+1})
        else:
            tweet_count.update({item:1})
    print(2)
for i in range(0,len(negative)):
    pattern = r'[0-9]'
    data = re.sub(pattern, ' ', negative[i][0])
    pattern = r"['™', '©', '®', '‰', '±', '¼', '½', '¾', '≡', '≈', '≥', '≤', '√', 'ⁿ', '¹', '²', '³', 'π', '°', '∞', 'µ', 'Σ', '☺', '☻', '•', '○', '♂', '♀', '↨', '↑', '↓', '→', '←', '↔', '£', '€', '$', '¢', '¥', 'ƒ', '₧', 'α', 'ß', 'δ', 'Ω', '►', '◄', '■', '▲', '▼', '§', '¶', '“', '”', '«', '»', '♥', 'º', 'œ', '•', '↻', '↺', 'Ø', 'Ñ', 'Ø', '±', 'Ù', '†', '§', '…', '‡', '¬', 'Û', 'Œ', 'Ú', '©', '´', '¾', '„', 'ª', 'µ', '¯', 'Ø³', 'Ø¹', 'ˆ', '®', 'Ø²', 'Ø°', 'º', 'â', '€', 'Ž','Ã','¯','Â','¿','ø','Ã','£']"
    data = re.sub(pattern, ' ', data)
    tokens = word_tokenize(data)
    ps = PorterStemmer()
    stemmed_words = [ps.stem(w) for w in tokens]
    stemmed_words = [w for w in stemmed_words if not w in stop_words]
    for item in stemmed_words:
        if item in vocab_neg.keys():
            vocab_neg.update({item:vocab_neg.get(item)+1})
        else:
            vocab_neg.update({item:1})
    tweet = " ".join(stemmed_words)
    cur.execute(("insert into stemmed_negative(txt) values('%s')")%(tweet))
    con.commit()
    stemmed_words = list(set(stemmed_words))
    for item in stemmed_words:
        if (item in tweet_count.keys()):
            tweet_count.update({item: tweet_count.get(item) + 1})
        else:
            tweet_count.update({item: 1})
    print(1)
geeky_file = open(r'C:\Users\Mohammadreza Rahmani\Desktop\geekyfile1.txt', 'wt')
geeky_file.write(str(vocab_pos))
geeky_file.close()
geeky_file = open(r'C:\Users\Mohammadreza Rahmani\Desktop\geekyfile2.txt', 'wt')
geeky_file.write(str(vocab_neg))
geeky_file.close()
geeky_file = open(r'C:\Users\Mohammadreza Rahmani\Desktop\tweet_count.txt', 'wt')
geeky_file.write(str(tweet_count))
geeky_file.close()