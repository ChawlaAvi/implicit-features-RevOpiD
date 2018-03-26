import pickle
import numpy as np


with open('list_of_list_of_list_of_reviews.pickle','rb') as h:
	unigrams = pickle.load(h)


f=open('extracted_after_part4.txt','r')
r=[]

for l in f:
	if l == '\n':
		pass
	else:
		r.append((l.strip()).split())

fo_number_with_sen_num={}

for idx,i in enumerate(unigrams):
	fo_number_with_sen_num[idx] = []



for idx1,i in enumerate(unigrams):  	    # i is of the format [[line1],[line2].....]
	for idx2,j in enumerate(i):				# j is of the format [word1,word2,word3.....]

		for idx3,k in enumerate(r):			# k is of the format ['opinion','feature']				

			if k[0] in j and k[1] in j:
									
				fo_number_with_sen_num[idx1].append(idx3)


f=open('reviews_and_their_features.txt','w')



for i in fo_number_with_sen_num:
	f.write(str(unigrams[i]))
	f.write('\n')	

	for j in fo_number_with_sen_num[i]:
		f.write(str(r[j]))


	f.write('\n')	
	f.write('\n')
	f.write('\n')	



f.close()

with open('fo_number_with_sen_num.pickle','wb') as h:
	pickle.dump(fo_number_with_sen_num,h)



