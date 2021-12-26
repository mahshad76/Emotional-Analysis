import psycopg2
from nltk.tokenize import word_tokenize
import re
from nltk.stem import PorterStemmer
import math
from nltk.corpus import stopwords

con=psycopg2.connect(
     host="localhost",
     database="postgres",
     user="postgres",
    password="mm123456"
 )
cur=con.cursor()

class Naive:
    def __init__(mysillyobject, input):
        mysillyobject.input= input

    def naive(abc):
        stop_words = set(stopwords.words('english'))
        cur.execute("select * from probabilities")
        probabilities = cur.fetchall()
        index = -1
        sum = 0.0
        with open(r'C:\Users\Mohammadreza Rahmani\Desktop\tweet_count.txt') as f:
            data = f.read()
        tweetcount = eval(data)
        vocab = list(tweetcount.keys())

        input=abc.input

        pattern = r'[0-9]'
        data = re.sub(pattern, ' ', input)
        sum = 0.0
        pattern1 = r"['™', '©', '®', '‰', '±', '¼', '½', '¾', '≡', '≈', '≥', '≤', '√', 'ⁿ', '¹', '²', '³', 'π', '°', '∞', 'µ', 'Σ']"
        pattern2 = r"['☺', '☻', '•', '○', '♂', '♀', '↨', '↑', '↓', '→', '←', '↔', '£', '€', '$', '¢', '¥', 'ƒ', '₧', 'α', 'ß', 'δ', 'Ω', '►', '◄', '■', '▲', '▼', '§', '¶', '“', '”', '«', '»', '♥', 'º', 'œ', '•', '↻', '↺', 'Ø', 'Ñ', 'Ø', '±', 'Ù', '†']"
        pattern3 = r"['§', '…', '‡', '¬', 'Û', 'Œ', 'Ú', '©', '´', '¾', '„', 'ª', 'µ', '¯', 'Ø³', 'Ø¹', 'ˆ', '®', 'Ø²', 'Ø°', 'º', 'â', '€', 'Ž']"
        data = re.sub(pattern1, ' ', data)
        data = re.sub(pattern2, ' ', data)
        data = re.sub(pattern3, ' ', data)
        tokens = word_tokenize(data)
        ps = PorterStemmer()
        stemmed_words = [ps.stem(w) for w in tokens]
        stemmed_words = [w for w in stemmed_words if not w in stop_words]
        for item in stemmed_words:
            index = -1
            for j in range(0, len(vocab)):
                if (vocab[j] == item):
                    index = j
                    #print(index)
                    break
            if (index != -1):
                sum += math.log((probabilities[j][0] / probabilities[j][1]), 10)
        if (sum > 0):
            return "positive"
            #print(sum)
        if (sum < 0):
            return "negative"
            #print(sum)
        if (sum == 0):
            return "neutral"
            #print(sum)