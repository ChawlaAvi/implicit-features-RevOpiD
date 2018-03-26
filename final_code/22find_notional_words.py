# to find the notional words.
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer

import string
import pickle

lemmatizer = WordNetLemmatizer()


with open('feature_list_with_keys_part_2.pickle','rb') as h:
	feature_list_with_keys = pickle.load(h)

only_features = [i for i in feature_list_with_keys]   # without values



punct = set(string.punctuation)




with open('list_of_list_of_list_of_reviews.pickle','rb') as h:
	unigrams = pickle.load(h)



'''
unigrams is of the following format
[
	[ 							}
		[(word1),(word2)....], 				}   for  one   
		[ [],[]...], 					}    review	
		[ [],[],[],[]....],....				}
	] 
]

'''

#print(unigrams[1:10])

notional_words_with_features = {}
		
for idx0,i in enumerate(only_features):					# idx0 is the key for the feature.
	print(idx0 , len(only_features))	
	a=[]	
	for idx1,j in enumerate( unigrams ):     		   	# j is for full review
		for idx2,k in enumerate(j):	   		   	# k is for a line in a review.
			
			if i in k:
				b=[]
				for l in k:
					b.append(l)
				a.append(b)

	
		
	notional_words_with_features[i] = a

'''
for i in notional_words_with_features:
	print(str(i) + " : " +  str(notional_words_with_features[i]))			
				
'''

with open('feature_notional_words_dict.pickle','wb') as h:
	pickle.dump(notional_words_with_features,h)		


