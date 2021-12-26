Python 3.7.4 (tags/v3.7.4:e09359112e, Jul  8 2019, 20:34:20) [MSC v.1916 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> with open(r'C:\Users\Mohammadreza Rahmani\Desktop\tweet_count.txt') as f:
    data = f.read()

    
>>> tweetcount = eval(data)
>>> vocab=list(tweetcount.keys())
>>> list=[]
>>> for item in vocab:
	list.append(item.encode('utf8'))

	
>>> with open(r'C:\Users\Mohammadreza Rahmani\Desktop\vocabulary_rbf.txt') as f:
    data = f.read()

    
Traceback (most recent call last):
  File "<pyshell#8>", line 1, in <module>
    with open(r'C:\Users\Mohammadreza Rahmani\Desktop\vocabulary_rbf.txt') as f:
FileNotFoundError: [Errno 2] No such file or directory: 'C:\\Users\\Mohammadreza Rahmani\\Desktop\\vocabulary_rbf.txt'
>>> file = open(r'C:\Users\Mohammadreza Rahmani\Desktop\vocab_rbf.txt', 'wt')
>>> geeky_file.write(list)
Traceback (most recent call last):
  File "<pyshell#10>", line 1, in <module>
    geeky_file.write(list)
NameError: name 'geeky_file' is not defined
>>> file.write(str(vocab))
629803
>>> with open(r'C:\Users\Mohammadreza Rahmani\Desktop\vocabrbf.txt') as f:
    data = f.read()

    
Traceback (most recent call last):
  File "<pyshell#15>", line 1, in <module>
    with open(r'C:\Users\Mohammadreza Rahmani\Desktop\vocabrbf.txt') as f:
FileNotFoundError: [Errno 2] No such file or directory: 'C:\\Users\\Mohammadreza Rahmani\\Desktop\\vocabrbf.txt'
>>> with open(r'C:\Users\Mohammadreza Rahmani\Desktop\vocab_rbf.txt') as f:
    data = f.read()

    
>>> v=eval(data)
>>> v[0]
'smile'
>>> v[1]
'put'
>>> from tensorflow.keras.preprocessing.text import one_hot
>>> voc_size=59756
>>> sentences=v
>>> onehot_repr=[one_hot(words,voc_size)for words in sentences]
>>> from tensorflow.keras.layers import Embedding
>>> from tensorflow.keras.preprocessing.sequence import pad_sequences
>>> from tensorflow.keras.models import Sequential
>>> import numpy as np
>>> sent_length=1
>>> embedded_docs=pad_sequences(onehot_repr,padding='pre',maxlen=sent_length)
>>> model=Sequential()
>>> model.add(Embedding(voc_size,100,input_length=sent_length))
>>> model.compile('adam','mse')
>>> embedded=model.predict(embedded_docs)
>>> m=[]
>>> for i in range(0,len(embedded)):
	a=map(sum, map(lambda l: map(float, l), zip(*embedded[i])))
	b=[]
	for item in a:
		b.append(item)
	m.append(b)

	
>>> import csv
>>> with open(r"C:\Users\Mohammadreza Rahmani\Desktop\embed_result22.csv", "w", newline="") as f:
	writer = csv.writer(f)
	writer.writerows(m)

	
>>> 
