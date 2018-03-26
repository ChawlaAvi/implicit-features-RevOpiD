from nltk import pos_tag
from nltk.stem import WordNetLemmatizer

import string
import pickle
import numpy as np

lemmatizer = WordNetLemmatizer()
punct = set(string.punctuation)


with open('list_of_list_of_list_of_reviews.pickle','rb') as h:
	unigrams = pickle.load(h)



all_words = {}
a=[]

for idx,i in enumerate(unigrams):
	print(idx , len(unigrams))
	for j in i:
		for k in j:
				
			a.append(k)

b=list(set(a))

for idx,i in enumerate(b):
	print(idx , len(b))
	all_words[i] = a.count(i)


with open('all_words_with_count.pickle','wb') as h:
	pickle.dump(all_words,h)



	
