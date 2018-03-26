import numpy as np
import pickle
import string
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

lemmatizer=WordNetLemmatizer()
punc = set(string.punctuation)
s=list(set(stopwords.words("english")))

r = []
f = open('cleandata1.txt', 'r')

for l in f:
	r.append(l[:-1])

f.close()

with open('all_together_in_a_dict.pickle','rb') as h:
	all_together= pickle.load(h)

feature_list = all_together.keys()
opinion_list  = []

for k in all_together:
	for i in all_together[k]:
		opinion_list.append(i)

unigrams =[]

for idx1,i in enumerate(r):
	b=[]
	for j in i.split('.')[:-1]:
		
		a=j.split()
		c=[]
		for idx2,j in enumerate(a):
			if j not in punc and j != 'and' and j != 'or' : 
				c.append(lemmatizer.lemmatize(j))
		
		b.append(c)		

	unigrams.append(b)		




opinion_list = [lemmatizer.lemmatize(i) for i in opinion_list if i not in punc and i not in s]
opinion_list = list(set(opinion_list))

feature_list = [lemmatizer.lemmatize(i) for i in feature_list if i not in punc and i not in s]
feature_list = list(set(feature_list))

#print(len(opinion_list))
num_of_opi_words=len(opinion_list)

modification_mat = np.zeros( (num_of_opi_words,len( feature_list )) ,dtype=int)# features->vertically , opinions-> horizontally

opinion_list_with_keys={}
feature_list_with_keys={}
count_opinions = 0
count_feature  = 0

for i in opinion_list:
	opinion_list_with_keys[i] = count_opinions
	count_opinions += 1

for i in feature_list:
	feature_list_with_keys[i] = count_feature
	count_feature += 1

del(opinion_list)
del(feature_list)

#print(opinion_list_with_keys)
#print(feature_list_with_keys)

for idx,i in enumerate(all_together):
	print(idx,len(all_together))									# here i is a feature
	try:
		column_num = feature_list_with_keys[i]						# column_num is the key of the feature in the matrix
		for op in all_together[i]:									# here j is the opinion linked with the feature.
			
			row_num    = opinion_list_with_keys[op]					# row_num is the key of the opinion in the matrix.

			for idx1,j in enumerate( unigrams ):     		   		# j is for full review  	  [[line1],[line2]....]
				for idx2,k in enumerate(j):	   		   				# k is for a line in a review.[word1,word2,...]
					
					if lemmatizer.lemmatize(i) in k and lemmatizer.lemmatize(op) in k:
		
						modification_mat[row_num][column_num] += 1				
	
	except:		
		pass

#print("modification_mat size = " ,modification_mat.shape)
#print("opinion_list_size = " , len(opinion_list_with_keys.keys()))
#print("feature_list_size = " , len(feature_list_with_keys.keys()))


f=open('modification_mat.txt','w')
for i in modification_mat:
	for j in i:
		a= str(j) + " "	
		f.write(a)
	f.write('\n')

f.close()


with open('opinion_list_with_keys.pickle','wb') as h:
	pickle.dump(opinion_list_with_keys,h)

with open('feature_list_with_keys.pickle','wb') as h:
	pickle.dump(feature_list_with_keys,h)

with open('modification_mat.pickle','wb') as h:
	pickle.dump(modification_mat,h)

with open('list_of_list_of_list_of_reviews.pickle','wb') as h:
	pickle.dump(unigrams,h)




