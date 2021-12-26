import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob
import psycopg2

con = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="mm123456"
)
cur = con.cursor()

po=0
ne=0
kh=0
l1=[]
stop_words = set(stopwords.words('english'))
print(stop_words)
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
file1 = open(r'C:\Users\Mohammadreza Rahmani\Desktop\happy.txt',encoding="utf8")
Lines = file1.readlines()
for line in Lines:
    s=line[2:]
    tweet = s.lower()
    tweet = re.sub(r"http\S+|www\S+|https\S+", '', tweet, flags=re.MULTILINE)
    tweet = re.sub(r'\@\w+|\#', '', tweet)
    tweet = re.sub(r'’', '', tweet)
    translator = re.compile('[%s]' % re.escape(string.punctuation))
    tweet=translator.sub(' ', tweet)
    tweet=add_space_between_emojies(tweet)
    tweet_tokens = word_tokenize(tweet)
    filtered_words = [w for w in tweet_tokens if not w in stop_words]
    tweet=" ".join(filtered_words)
    analysis = TextBlob(tweet)
    if(analysis.sentiment.polarity>0):
        query = "insert into positive(txt) values(%s)" % ("'"+tweet+"'")
        cur.execute(query)
        con.commit()
    if (analysis.sentiment.polarity < 0):
        query = "insert into negative(txt) values(%s)" % ("'" + tweet + "'")
        cur.execute(query)
        con.commit()
    if (analysis.sentiment.polarity == 0):
        query = "insert into neutral(txt) values(%s)" % ("'" + tweet + "'")
        cur.execute(query)
        con.commit()