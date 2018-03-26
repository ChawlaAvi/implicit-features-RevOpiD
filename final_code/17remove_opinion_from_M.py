import pickle
import numpy as np

f=open('cleandata1.txt','r')
length = 0

for l in f:
	length += 1


with open('opinion_list_with_keys_part_1.pickle','rb') as h:
	opinion_list_with_keys=pickle.load(h)

with open('feature_list_with_keys_part_1.pickle','rb') as h:
	feature_list_with_keys=pickle.load(h)

with open('modification_mat_part_3.pickle','rb') as h:
	modification_mat=pickle.load(h)	


feature_list = feature_list_with_keys.keys()
opinion_list = opinion_list_with_keys.keys()

count_opinion = len(opinion_list)
count_feature = len(feature_list)

#print(np.sum(modification_mat,axis=0))

total_links_for_opinion = (np.sum(modification_mat,axis=1)).tolist()
min_count = 0#  length / 15

to_be_retained=[]   					

for idx1,i in enumerate(total_links_for_opinion):
	if i > min_count :
		to_be_retained.append(idx1)
		
modified_opinion={}

for idx1,i in enumerate(to_be_retained):
	modified_opinion[str(list(opinion_list_with_keys.keys())[list(opinion_list_with_keys.values()).index(i)])] = idx1

#print(to_be_removed)

modification_mat = modification_mat[to_be_retained , :]
print(modification_mat.shape)

with open('modification_mat_part_4.pickle','wb') as h:
	pickle.dump(modification_mat,h)	

with open('opinion_list_with_keys_part_2.pickle' , 'wb') as h:
	pickle.dump(modified_opinion,h)

f=open('modification_mat_part4_.txt','w')
for i in modification_mat:
	for j in i:
		a= str(j) + " "	
		f.write(a)
	f.write('\n')

f.close()


		
