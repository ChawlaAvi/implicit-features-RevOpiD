import pickle
import numpy as np
import string

from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import stopwords
import treetaggerwrapper


tagger = treetaggerwrapper.TreeTagger(TAGLANG='en')

lemmatizer=WordNetLemmatizer()
punc = set(string.punctuation)
s=set(stopwords.words("english"))

not_req = set(['not','it','its','''it's''' , 'and','''weren't''','''haven't''' , 'or','u','etc','''you're''','that','''that's''','okay','''don't''','dont','cant','''can't''','''i've''','oh','ohh','''we've''','have','we',
'were','could','''couldn't''','couldnt','you','didnt','''didn't''','did','does','doesnt', '''doesn't''','should','''shouldn't''','your',
'''yours''','''your's''','wont','''won't''','a','an','the','our','ours','''our's''','as','being','been','he','him','himself','she','her'
,'herself','only','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])

not_required = punc | s | not_req
not_required = list(not_required)


with open('opinion_list_with_keys.pickle','rb') as h:
	opinion_list_with_keys=pickle.load(h)

with open('feature_list_with_keys_part_1.pickle','rb') as h:
	feature_list_with_keys=pickle.load(h)

with open('modification_mat_part_1.pickle','rb') as h:
	modification_mat=pickle.load(h)

r = []
f = open('cleandata1.txt', 'r')

for l in f:
	r.append(l[:-1])

f.close()

r_with_pos=[]

for idx,i in enumerate(r):
	b=[]
	for j in i.split('.')[:-1]:
		anay = j.split()
		a=[]
		for k in anay:
			gotiya = []
			tags = tagger.tag_text(k)
			tag = treetaggerwrapper.make_tags(tags)
			tag = tag[0][1]
			gotiya.append(k)
			gotiya.append(tag)
			a.append(gotiya)

		b.append(a)		
	r_with_pos.append(b)

'''
r_with_pos is of the following format
[
	[ 							}
		[(word1,pos),(word2,pos)....], 			}  for one   
		[ [],[]...], 					}   review	
		[ [],[],[],[]....],....				}
	] 
]

'''



opinion_list = opinion_list_with_keys.keys()   # this list only consists of the opinions extracted (no keys are present)
feature_list = feature_list_with_keys.keys()   # this list only consists of the features extracted (no keys are present)

count_opinions = len(opinion_list)
count_features = len(feature_list) 

not_found_any_adj = []   # will be used to store locations of sentences where no features where found.

'''
idx1 -> this is for the review number
idx2 -> this is for sentence number in that particular sentence
idx3 -> this is for the word number in that  sentence

'''

for idx,i in enumerate(feature_list):
	print(idx,len(feature_list))
	
	for idx1,j in enumerate( r_with_pos ):     		   	# j is for full review
		for idx2,k in enumerate(j):	   		   	# k is for a line in a review.
			for idx3,l in enumerate(k):		  	# l is of the format ('word','pos_tag')
				
				if lemmatizer.lemmatize(l[0],'v') == lemmatizer.lemmatize(i,'v') :
					
					a= idx3 - 1
					flag1,flag2,flag3 = 0,0,0
					while a>=0 and flag1 == 0  : 
						
						p = a
						try:
							tags = tagger.tag_text(lemmatizer.lemmatize(k[a][0]))
							tag = treetaggerwrapper.make_tags(tags)
							tag_for_a = tag[0][1]
						except:
							tag_for_a = k[a][1]	

						if (tag_for_a == 'NN' or tag_for_a == 'NNS' or tag_for_a == 'NNP' or tag_for_a == 'NNPS') and k[a][0] not in not_required:		
							
							if (a < len(k)-1) :    # atleast second last in the sentence.
								try:
									tags = tagger.tag_text(lemmatizer.lemmatize(k[a][0]))
									tag = treetaggerwrapper.make_tags(tags)
									tag_for_next_a = tag[0][1]
								except:
									tag_for_next_a = k[a+1][1]

								if (tag_for_next_a == 'NN' or tag_for_next_a == 'NNS' or tag_for_next_a == 'NNP' or tag_for_next_a == 'NNPS') and k[a+1][0] not in not_required:
									flag1 == 1
							
							if flag1 == 0:
								
								
								try:
									tags = tagger.tag_text(lemmatizer.lemmatize(k[p][0]))
									tag = treetaggerwrapper.make_tags(tags)
									tag_for_p = tag[0][1]
								except:
									tag_for_p = k[p][1]
								
								while p>=0 and (tag_for_p == 'NN' or tag_for_p == 'NNS' or tag_for_p == 'NNP' or tag_for_p == 'NNPS'):
									
									p -= 1
									if p >=0:
										word = lemmatizer.lemmatize(k[p][0])
										try:
											tags = tagger.tag_text(lemmatizer.lemmatize(word))
											tag = treetaggerwrapper.make_tags(tags)
											tag_for_p = tag[0][1]
										
										except:
											tag_for_p = k[p][1]
								
								if p>=0 and (tag_for_p == 'JJ' or tag_for_p == 'JJS' or tag_for_p == 'JJS' or tag_for_p == 'RB' or tag_for_p == 'RBS' or tag_for_p == 'RBR'):		
										
										word = lemmatizer.lemmatize(k[p][0])
										try:
											tags = tagger.tag_text(lemmatizer.lemmatize(word))
											tag = treetaggerwrapper.make_tags(tags)
											tag_for_p = tag[0][1]
										except:
											tag_for_p = k[p][1]

										while p>=0 and (tag_for_p == 'JJ' or tag_for_p == 'JJS' or tag_for_p == 'JJS' or tag_for_p == 'RB' or tag_for_p == 'RBS' or tag_for_p == 'RBR' or tag_for_p =='CC' or tag_for_p ==','):
											
											if (tag_for_p == 'JJ' or tag_for_p == 'JJS' or tag_for_p == 'JJS' or tag_for_p == 'RB' or tag_for_p == 'RBS' or tag_for_p == 'RBR' or tag_for_p =='CC' or tag_for_p ==','):
												flag2 = 1
												print("1",i,k[p][0] ,tag_for_p, end = ' ')
												k[p][0] = lemmatizer.lemmatize(k[p][0])
												if k[p][0] in opinion_list :
													x = opinion_list_with_keys[k[p][0]]
													y = feature_list_with_keys[i]
													modification_mat[x][y] += 1
										
												else:
													opinion_list_with_keys[k[p][0]]= count_opinions
													count_opinions += 1
													x = opinion_list_with_keys[k[p][0]]
													y = feature_list_with_keys[i]
													new_row = np.zeros((1,count_features) , dtype = int)
													modification_mat = np.append(modification_mat,new_row,axis = 0)
													modification_mat[x][y] += 1
												
											p -= 1
											word = lemmatizer.lemmatize(k[p][0])
											try:
												tags = tagger.tag_text(lemmatizer.lemmatize(word))
												tag = treetaggerwrapper.make_tags(tags)
												tag_for_p = tag[0][1]
											except:
												tag_for_p = k[p][1]

							
						a = p-1

					if flag2 == 0:
						a = idx3 + 1
							
						while a< len(k) and flag2 == 0:
							
							k[a][0] = lemmatizer.lemmatize(k[a][0])
							try:
								tags = tagger.tag_text(lemmatizer.lemmatize(k[a][0]))
								tag = treetaggerwrapper.make_tags(tags)
								tag_for_a = tag[0][1]
							except:
								tag_for_a = k[a][1]	

							if (tag_for_a == 'JJ' or tag_for_a == 'JJS' or tag_for_a == 'JJS' or tag_for_a == 'RB' or tag_for_a == 'RBS' or tag_for_a == 'RBR' ):
								flag2 = 1
								print("2",i,k[a][0] ,tag_for_a, end = ' ')
								k[a][0] = lemmatizer.lemmatize(k[a][0])
								if k[a][0] in opinion_list :
										x = opinion_list_with_keys[k[a][0]]
										y = feature_list_with_keys[i]
										modification_mat[x][y] += 1
										
								else:
										opinion_list_with_keys[k[a][0]]= count_opinions
										count_opinions += 1
										x = opinion_list_with_keys[k[a][0]]
										y = feature_list_with_keys[i]
										new_row = np.zeros((1,count_features) , dtype = int)
										modification_mat = np.append(modification_mat,new_row,axis = 0)
										modification_mat[x][y] += 1

						


							a += 1

	print('\n')


index_to_be_removed =[]
index_to_be_retained =[]
for i in opinion_list_with_keys:
	try :
		tag = word_pos_dict[i]	

	except:
		tag = pos_tag([i])[0][1]

	if 	tag != 'JJ' and tag != 'JJR' and tag != 'JJS' and tag != 'RB' and tag != 'RBR' and tag != 'RBS':
		index_to_be_removed.append(opinion_list_with_keys[i])
		#print( i , tag ,feature_list_with_keys[i])

	else:
		index_to_be_retained.append(opinion_list_with_keys[i])
			

#print("remove" , index_to_be_removed)									

modification_mat = modification_mat[ index_to_be_retained , : ]

new_opinion_list_with_keys = {}

for idx,i in enumerate(index_to_be_retained):
		value = str(list(opinion_list_with_keys.keys())[list(opinion_list_with_keys.values()).index(i)])
		new_opinion_list_with_keys[value] = idx 

print(new_opinion_list_with_keys.keys())		


			
with open('modification_mat_part_2.pickle','wb') as h:
	pickle.dump(modification_mat,h)	

with open('opinion_list_with_keys_part_1.pickle','wb') as h:
	pickle.dump(opinion_list_with_keys,h)

f=open('modification_mat_part2_.txt','w')
for i in modification_mat:
	for j in i:
		a= str(j) + " "	
		f.write(a)
	f.write('\n')

f.close()

	
	
