import psycopg2
from nltk.tokenize import word_tokenize
import re
from nltk.stem import PorterStemmer

con=psycopg2.connect(
     host="localhost",
     database="postgres",
     user="postgres",
    password="mm123456"
 )
cur=con.cursor()

#cur.execute("CREATE TABLE pos_test(polarity text)")
#cur.execute("CREATE TABLE neg_test(polarity text)")
#cur.execute("CREATE TABLE neg_distinct(txt text)")
#cur.execute("CREATE TABLE pos_distinct(txt text)")
#cur.execute("CREATE TABLE probabilities(pos_prob double precision,neg_prob double precision)")
#cur.execute("CREATE TABLE vocabulary(txt text)")
#cur.execute("CREATE TABLE idf(num double precision)")
#cur.execute("CREATE TABLE stemmed_positive(txt text)")
#cur.execute("CREATE TABLE stemmed_negative(txt text)")
#cur.execute("CREATE TABLE tf_idf_pos(str text)")
#cur.execute("CREATE TABLE tf_idf_neg(str text)")
cur.execute("CREATE TABLE knn_pos(txt text)")
cur.execute("CREATE TABLE knn_neg(txt text)")
#cur.execute("CREATE TABLE y_network(polarity smallint)")
#cur.execute("CREATE TABLE tf_idf_trainrbf(str text)")
#cur.execute("CREATE TABLE hello_pos(txt text)")
#cur.execute("CREATE TABLE hello_neg(txt text)")

con.commit()

