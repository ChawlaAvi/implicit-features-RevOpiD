import numpy as np
import pickle


with open('feature_notional_words_dict.pickle','rb') as h:
	notional_words_with_features= pickle.load(h)

feature_list_with_keys = {}
j=0
for i in notional_words_with_features:
	feature_list_with_keys[i] = j
	j += 1



all_unique_notional_words = []

for i in feature_list_with_keys:
	try:
		for j in notional_words_with_features[i]:
			for k in j:
				if k != i:			
					all_unique_notional_words.append(k)

	except:
		pass	
	
all_unique_notional_words = list(set(all_unique_notional_words))

all_unique_notional_words_with_keys={}

j=0
for i in all_unique_notional_words:
	all_unique_notional_words_with_keys[i] = j
	j += 1

co_occurrence_matrix = np.zeros( (len(feature_list_with_keys.keys()) , len(all_unique_notional_words)) ,dtype = int)

'''

for idx,i in enumerate(feature_list_with_keys):
	print(idx , len(feature_list_with_keys))
	try : 
		for j in all_unique_notional_words_with_keys:
		
			for k in notional_words_with_features[i]:
				for l in k:
					if l == j:
						co_occurrence_matrix[feature_list_with_keys[i]][all_unique_notional_words_with_keys[j]] += 1
	except :
		pass
		

'''


for idx,i in enumerate(feature_list_with_keys):
	print(idx , len(feature_list_with_keys))
	try:
		for j in notional_words_with_features[i]:
			for k in j:
				if k != i:
					co_occurrence_matrix[feature_list_with_keys[i]][all_unique_notional_words_with_keys[k]] += 1
				
	except:
		pass




f=open('co_occurrence_matrix.txt','w')

for i in co_occurrence_matrix:
	for j in i:
		a= str(j) + " "	
		f.write(a)
	f.write('\n')

f.close()



with open('co_occurrence_matrix_C.pickle' ,'wb') as h:
	pickle.dump(co_occurrence_matrix,h)


with open('notional_words_used_for_matrix_C.pickle','wb') as h:
	pickle.dump(all_unique_notional_words_with_keys,h)


with open('features_used_for_matrix_C.pickle','wb') as h:
	pickle.dump(feature_list_with_keys,h)




			
		






