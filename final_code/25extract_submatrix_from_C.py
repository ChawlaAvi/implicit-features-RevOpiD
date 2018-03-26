import pickle
import numpy as np

from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

with open('all_words_with_count.pickle','rb') as h:
	all_words = pickle.load(h)

with open('full_sentences.pickle','rb') as h:
		sent = pickle.load(h)

f=open('final_answers.txt','w')
	
with open('candidate_features.pickle','rb') as h:
	candidate_features = pickle.load(h)  
 # list of list where each inner list represents candidate features for the sentence having no explicit features.

with open('revnum_and_linenum_for_no_explicit_features.pickle','rb') as h:
	rev_num_and_line_num = pickle.load(h)

with open('list_of_list_of_list_of_reviews.pickle','rb') as h:
	unigrams = pickle.load(h)

with open('co_occurrence_matrix_C.pickle' ,'rb') as h:
	co_occurrence_matrix = pickle.load(h)

with open('notional_words_used_for_matrix_C.pickle','rb') as h:
	all_unique_notional_words_with_keys = pickle.load(h)

with open('features_used_for_matrix_C.pickle','rb') as h:
	feature_list_with_keys = pickle.load(h)

with open('synonym_dict.pickle','rb') as h:
	synonym_dict = pickle.load(h)	

#print(sent[4][3])
#quit()	

for idx,i in enumerate(rev_num_and_line_num) :
	try:
		print(idx , len(rev_num_and_line_num))
		words_present1 = unigrams[i[0]][i[1]]
		candidates = candidate_features[idx]
		#print(words_present,candidates)
		#continue
	
		column_numbers     = []

		row_numbers        = []

		words_present = words_present1 #+ synonym_dict[idx]
		words_present = list(set(words_present))

		for idx1,j in enumerate(words_present):
			if j in all_unique_notional_words_with_keys:
				column_numbers.append(all_unique_notional_words_with_keys[j])	

	
		for idx1,j in enumerate(candidates):
			row_numbers.append(feature_list_with_keys[j])



		submatrix = co_occurrence_matrix[row_numbers , :][: , column_numbers]
		#print(count , len(count))
	
		score=[]
		for idx1,j in enumerate(candidates):
			row_for_a_feature = submatrix[idx1,:]
			sum=0
			
			#print(j , row_for_a_feature )
			#continue
			for idx2,k in enumerate(row_for_a_feature):
				index_in_column_numbers = column_numbers[idx2]
				word = list(all_unique_notional_words_with_keys.keys())[list(all_unique_notional_words_with_keys.values()).index(index_in_column_numbers)]
				sum += k/all_words[lemmatizer.lemmatize(word)]	
				
					
			score.append(sum)
			
		try :	
			f.write('[')
			for l in words_present1:
				
				f.write(l) 
				f.write(',')

			f.write(']')
			f.write('[')
			

			for l in sent[i[0]][i[1]].split():
				f.write(l)
				f.write(',')

			f.write(']')
			
			f.write(candidates[score.index(max(score))])	
			f.write('\n')
			f.write('\n')
		except:
			
			f.write("not found") 

			f.write('\n')	
			f.write('\n')
		
	except:
		pass				
		

f.close()

