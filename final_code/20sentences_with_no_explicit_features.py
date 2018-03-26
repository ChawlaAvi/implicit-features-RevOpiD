from nltk import pos_tag
import pickle
import string
from nltk.stem import WordNetLemmatizer

punct = set(string.punctuation)
lemmatizer = WordNetLemmatizer()


r = []
f = open('cleandata1.txt', 'r')

for l in f:
	r.append(l[:-1])

f.close()



with open('final_adjective_list.pickle','rb') as h:
	adj_list = pickle.load(h)

with open('cleandata1_pos.pickle','rb') as h:
	word_pos_dict=pickle.load(h)


with open('list_of_list_of_list_of_reviews.pickle','rb') as h:
	unigrams = pickle.load(h)


r_with_pos=[]

for idx,i in enumerate(r):
	b=[]
	for j in i.split('.')[ : -1]:
		
		a=pos_tag(j.split())
		b.append(a)		

	r_with_pos.append(b)




'''
unigrams is of the following format
[
	[ 							}
		[(word1,pos),(word2,pos)....], 			}  for one   
		[ [],[]...], 					}   review	
		[ [],[],[],[]....],....				}
	] 
]

'''

rev_num_and_line_num = []



for idx1,j in enumerate( r_with_pos ):     		   	# j is for full review
	print(idx1 , len(r_with_pos))	
	for idx2,k in enumerate(j):	   		   	# k is for a line in a review.

		flag_for_imp = 1
		a=[]
		
		for idx3,l in enumerate(k):		  	# l is of the format ('word','pos_tag')
			
			#if (l[1] == 'NN' or l[1] == 'NNS' or l[1] == 'NNP' or l[1] == 'NNPS') and l[0] not in adj_list :
			try:
				#tag = word_pos_dict[l[0]]
				tags = tagger.tag_text(lemmatizer.lemmatize(l[0]))
				tag = treetaggerwrapper.make_tags(tags)
				tag = tag[0][1]
			except:
				tag = l[1]	

			if (tag == 'NN' or tag == 'NNS' or tag == 'NNP' or tag == 'NNPS'):	
				flag_for_imp = 0 
				
			
		if flag_for_imp == 1:
			
			rev_num_and_line_num.append([idx1,idx2])


#print(r_with_pos)	

with open('revnum_and_linenum_for_no_explicit_features.pickle','wb') as h:
	pickle.dump(rev_num_and_line_num,h)



#with open('opinions_for_implicit_sentence.pickle','wb') as h:
#	pickle.dump(opinions_in_that_sentence,h)


#with open('rev_num_and_line_num_for_implicit.pickle','wb') as h:
#	pickle.dump(rev_num_and_line_num,h)



#print(len(r_with_pos))	
						

