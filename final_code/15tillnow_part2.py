import pickle
import numpy as np


with open('opinion_list_with_keys_part_1.pickle','rb') as h:
	a=pickle.load(h)

with open('feature_list_with_keys_part_1.pickle','rb') as h:
	b=pickle.load(h)

with open('modification_mat_part_2.pickle','rb') as h:
	modification_mat=pickle.load(h)	

f=open('extracted_after_part2.txt','w')

for idx1,i in enumerate(modification_mat):
	for idx2,j in enumerate(i) :
		if modification_mat[idx1][idx2] != 0:
			
			f.write(str(list(a.keys())[list(a.values()).index(idx1)]) + " " + str(list(b.keys())[list(b.values()).index(idx2)]) )
			f.write('\n')
	f.write('\n')

		



print("opinions count")
x=modification_mat.sum(axis=1)

for idx,i in enumerate(x.tolist()):
	print("[ " , str(list(a.keys())[list(a.values()).index(idx)]) , i , " ] ",end ='  ')

print("features count" )
y=modification_mat.sum(axis=0)
print('\n \n ')
for idx,i in enumerate(y.tolist()):
	print("[ ", str(list(b.keys())[list(b.values()).index(idx)]) , i ," ]", end ='  ')
