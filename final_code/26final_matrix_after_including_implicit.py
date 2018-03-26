import pickle
import csv


with open('fo_number_with_sen_num.pickle','rb') as h:
	fo_number_with_sen_num = pickle.load(h)

f=open('extracted_after_part4.txt','r')
r=[]

for l in f:
	if l == '\n':
		pass
	else:
		r.append((l.strip()).split())

opinion_feature_id ={}
i=0
for j in r:
	opinion_feature_id[' '.join(j)] = i
	i += 1

with open('length_of_op.pickle','wb') as h:
	pickle.dump(i,h)	

with open('modification_mat_part_4.pickle' ,'rb') as h:
		modification_mat = pickle.load(h)

with open('implicit_extracted.pickle','rb') as h:
		final_features_found = pickle.load(h)

with open('revnum_and_linenum_for_no_explicit_features.pickle','rb') as h:
	rev_num_and_line_num = pickle.load(h)

with open('list_of_list_of_list_of_reviews.pickle','rb') as h:
	unigrams = pickle.load(h)  # it is made from cleandata file and it is a list of list.

no_of_reviews = len(unigrams)

with open('feature_list_with_keys_part_2.pickle','rb') as h:
	feature_list_with_keys=pickle.load(h)

with open('opinion_list_with_keys_part_2.pickle','rb') as h:
	opinion_list_with_keys=pickle.load(h)	

with open('synonym_dict.pickle' , 'rb') as h:
		synonym_dict = pickle.load(h)
i=1


feature_list = feature_list_with_keys.keys()
opinion_list = opinion_list_with_keys.keys()
count = 0

for idx,i in enumerate(rev_num_and_line_num):
	print(idx,len(rev_num_and_line_num))
	try:
		feature_found = final_features_found[idx]
		
		words_present = synonym_dict[idx]
		# print(count)
		# count += 1
		for word in words_present:
			if word in opinion_list:
				modification_mat[opinion_list_with_keys[word]][feature_list_with_keys[feature_found]] += 1
				opinion_plus_feature = str(word) + " " + str(feature_found)
				opinion_plus_feature = ' '.join(opinion_plus_feature.split())
				try:	
					its_id = opinion_feature_id[opinion_plus_feature]
					print(count )
					count +=1
				except:
					pass

					

				fo_number_with_sen_num[i[0]].append(its_id)
				
	except:
		
		pass



with open('modification_mat_part_5.pickle','wb') as h:
		pickle.dump(modification_mat,h)

		
for i in fo_number_with_sen_num:
	
	x = fo_number_with_sen_num[i]
	x= list(set(x))
	fo_number_with_sen_num[i] = x


with open('fo_number_with_sen_num_part1.pickle','wb') as h:
	pickle.dump(fo_number_with_sen_num,h)

