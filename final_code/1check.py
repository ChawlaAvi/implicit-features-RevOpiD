from nltk import tokenize
import re
import pickle

PROD = 'BeautyProd18'
f = 'text_0_'+PROD+'.txt'
f = open(f)

list_of_lists=[]
for i,review in enumerate(f):
	if i%2==0:
		
		r = re.compile(r'([.,/#!$%^&*;:{}=_`~()-])[.,/#!$%^&*;:{}=_`~()-]+')
		review_formatted = r.sub(r'\1', review)
		review_formatted=re.sub(r'([\.,/#!$%^&*;:{}=_`~()-])([a-zA-Z])', r'\1 \2', review_formatted)
		list_of_lists.append(tokenize.sent_tokenize(review_formatted))

# for i in list_of_lists:
# 	for j in i:
# 		print(j)

with open("tokenized_sentences.pickle",'wb') as h:
		pickle.dump(list_of_lists,h)
