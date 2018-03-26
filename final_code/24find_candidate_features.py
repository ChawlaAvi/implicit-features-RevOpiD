import pickle
import string
import numpy as np
from PyDictionary import PyDictionary
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag


with open('revnum_and_linenum_for_no_explicit_features.pickle','rb') as h:
	rev_num_and_line_num = pickle.load(h)

with open('feature_list_with_keys_part_2.pickle','rb') as h:
	feature_list_with_keys = pickle.load(h)

with open('opinion_list_with_keys_part_2.pickle','rb') as h:
	opinion_list_with_keys = pickle.load(h)

with open('modification_mat_part_4.pickle','rb') as h:
	modification_matrix = pickle.load(h)

with open('cleandata1_pos.pickle','rb') as h:
	word_pos_dict=pickle.load(h)

flag = 1
try :
	with open('synonym_dict.pickle' , 'rb') as h:
		synonym_dict = pickle.load(h)

except:
	flag = 0
	synonym_dict = {}
	


print("flag = ", flag )

f= open('non_single_words.txt','w')

lem = WordNetLemmatizer()
py=PyDictionary()
punct = set(string.punctuation)

def get_synonyms(words):
	a=[]
	for j in words:
		try:
			print("try")
			p=py.synonym(j)

			for k in p:
				a.append(k)
				a.append(lem.lemmatize(k))

		except:
			print("except" )
			f.write(str(j))
			f.write('\n \n')
			pass

	return a		


with open('list_of_list_of_list_of_reviews.pickle','rb') as h:
	unigrams = pickle.load(h)


#print(sentences[rev_num_and_line_num[0][0]][rev_num_and_line_num[0][1]])

candidate_features=[]
need_to_store = 0
for idx,i in enumerate(rev_num_and_line_num):
	try:
		print(idx , len(rev_num_and_line_num))
		
		
		words_present = unigrams[i[0]][i[1]]
		words_present_jj = []
		for i in words_present:
			try:
				#tag=word_pos_dict[i]
				tags = tagger.tag_text(lemmatizer.lemmatize(i))
				tag = treetaggerwrapper.make_tags(tags)
				tag = tag[0][1]
			except:
				tag = pos_tag([i])[0][1]

			if tag == 'JJ' or tag == 'JJR' or tag == 'JJS' or tag == 'RBR' or tag == 'RBS' or tag == 'RB' :	
				words_present_jj.append(i)

		if len(words_present_jj) != 0:
			words_present = words_present_jj


		if flag == 0 or len(synonym_dict.keys()) != len(rev_num_and_line_num):
			words_present += get_synonyms(words_present)
			words_present = list(set(words_present))
			words_present += get_synonyms(words_present)
			words_present = list(set(words_present))
			words_present += get_synonyms(words_present)
			words_present = list(set(words_present))
			synonym_dict[idx] = words_present
			need_to_store = 1
		
		else : 
			words_present = synonym_dict[idx]


		a=[]
		for j in words_present:
			if j in opinion_list_with_keys.keys() :
				print(j)
				ind = np.nonzero(modification_matrix[opinion_list_with_keys[j] , :])
				for k in ind[0].tolist():
					#if modification_matrix[opinion_list_with_keys[j]][k] > 5 :
						a.append(list(feature_list_with_keys.keys())[list(feature_list_with_keys.values()).index(k)])

		candidate_features.append(a)

	except:
		pass


#for i,j in enumerate(rev_num_and_line_num):
#	print(str(sentences[j[0]][j[1]])+ " : " ,str(candidate_features[i] ) )	

with open('candidate_features.pickle','wb') as h:
	pickle.dump(candidate_features,h)

if need_to_store == 1:
	with open('synonym_dict.pickle' , 'wb') as h:
		pickle.dump(synonym_dict,h)




	



