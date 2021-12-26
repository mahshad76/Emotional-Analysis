import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import psycopg2
import string
from textblob import TextBlob

con = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="mm123456"
)
cur = con.cursor()
list1=[]
list2=[]
stop_words = set(stopwords.words('english'))
def add_space_between_emojies(text):
  EMOJI_PATTERN = re.compile(
    "(["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "])"
  )
  text = re.sub(EMOJI_PATTERN, r' \1 ', text)
  return text
def load_dataset(filename, cols):
    dataset = pd.read_csv(filename, encoding='latin-1')
    dataset.columns = cols
    return dataset
def remove_unwanted_cols(dataset, cols):
    for col in cols:
        del dataset[col]
    return dataset
dataset = load_dataset(r"C:\Users\Mohammadreza Rahmani\Desktop/training.csv", ['target', 't_id', 'created_at', 'query', 'user', 'text'])
n_dataset = remove_unwanted_cols(dataset, ['t_id', 'created_at', 'query', 'user'])
for i in range(0,1599999):
    break
    s = n_dataset.iat[i, 1]
    tweet = s.lower()
    tweet = re.sub(r"http\S+|www\S+|https\S+", '', tweet, flags=re.MULTILINE)
    tweet = re.sub(r'\@\w+|\#', '', tweet)
    tweet = re.sub(r'’', '', tweet)
    translator = re.compile('[%s]' % re.escape(string.punctuation))
    tweet = translator.sub(' ', tweet)
    tweet = add_space_between_emojies(tweet)
    tweet_tokens = word_tokenize(tweet)
    filtered_words = [w for w in tweet_tokens if not w in stop_words]
    tweet = " ".join(filtered_words)
    analysis = TextBlob(tweet)
    if(n_dataset.iat[i,0]==0):
        if (analysis.sentiment.polarity > 0):
            query = "insert into neg_pos(txt) values(%s)" % ("'" + tweet + "'")
            cur.execute(query)
            con.commit()
        if (analysis.sentiment.polarity < 0):
            query = "insert into neg_neg(txt) values(%s)" % ("'" + tweet + "'")
            cur.execute(query)
            con.commit()
        if (analysis.sentiment.polarity == 0):
            query = "insert into neg_nu(txt) values(%s)" % ("'" + tweet + "'")
            cur.execute(query)
            con.commit()
            print(1)
    if (n_dataset.iat[i, 0] == 4):
        if (analysis.sentiment.polarity > 0):
            query = "insert into pos_pos(txt) values(%s)" % ("'" + tweet + "'")
            cur.execute(query)
            con.commit()
        if (analysis.sentiment.polarity < 0):
            query = "insert into pos_neg(txt) values(%s)" % ("'" + tweet + "'")
            cur.execute(query)
            con.commit()
        if (analysis.sentiment.polarity == 0):
            query = "insert into pos_nu(txt) values(%s)" % ("'" + tweet + "'")
            cur.execute(query)
            con.commit()
            print(2)

#print(n_dataset.iat[0,0])