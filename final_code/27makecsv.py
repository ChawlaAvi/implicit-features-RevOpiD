import csv
import pickle
import numpy as np

with open('fo_number_with_sen_num_part1.pickle','rb') as h:
	fo_number_with_sen_num = pickle.load(h)

with open('list_of_list_of_list_of_reviews.pickle','rb') as h:
	unigrams = pickle.load(h)  # it is made from cleandata file and it is a list of list.

with open('length_of_op.pickle','rb') as h:
	length = pickle.load(h)	

no_of_reviews = len(unigrams)

final_mat = np.zeros( (no_of_reviews,(length+1) ) ,dtype = int)
initial = 1001
for idx,i in enumerate(fo_number_with_sen_num):
	final_mat[idx][0] = initial
	for j in fo_number_with_sen_num[i]:
		final_mat[idx][j+1] = 1
	initial += 1

with open('finaldata.csv', 'w') as csvfile:
    text = csv.writer(csvfile)
    # for i in final_mat:
    text.writerows(final_mat)

with open('final_opinion_matrix.pickle','wb') as h:
	pickle.dump(final_mat,h)






