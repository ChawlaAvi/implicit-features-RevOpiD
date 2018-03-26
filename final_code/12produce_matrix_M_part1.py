import pickle
import numpy as np
import string

from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import stopwords
import treetaggerwrapper


tagger = treetaggerwrapper.TreeTagger(TAGLANG='en')

lemmatizer = WordNetLemmatizer()
punc = set(string.punctuation) ^ set(',')
s= set(stopwords.words("english")) ^ set(('and' , 'or'))

not_req = set(['not','it','its','''it's''' ,'''weren't''','''haven't''' ,'u','etc','''you're''','that','''that's''','okay','''don't''','dont','cant','''can't''','''i've''','oh','ohh','''we've''','have','we',
'were','could','''couldn't''','couldnt','you','didnt','''didn't''','did','does','doesnt', '''doesn't''','should','''shouldn't''','your',
'''yours''','''your's''','wont','''won't''','a','an','the','our','ours','''our's''','as','being','been','he','him','himself','she','her'
,'herself','only','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])

not_required = punc | s | not_req
not_required = list(not_required)


with open('final_adjective_list.pickle','rb') as h:
	adj_list = pickle.load(h)

with open('opinion_list_with_keys.pickle','rb') as h:
	opinion_list_with_keys=pickle.load(h)

with open('feature_list_with_keys.pickle','rb') as h:
	feature_list_with_keys=pickle.load(h)

with open('modification_mat.pickle','rb') as h:
	modification_mat=pickle.load(h)

with open('cleandata1_pos.pickle','rb') as h:
	word_pos_dict=pickle.load(h)

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
		[ [],[]...], 							}   review	
		[ [],[],[],[]....],....					}
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

for idx,i in enumerate(opinion_list):
	print(idx , len(opinion_list),end=' ')
	for idx1,j in enumerate( r_with_pos ):     		   	# j is for full review
		for idx2,k in enumerate(j):	   		   	# k is for a line in a review.
			for idx3,l in enumerate(k):		  	# l is of the format ('word','pos_tag')
				
				if lemmatizer.lemmatize(l[0],'v') == lemmatizer.lemmatize(i,'v') :
					
					b = idx3 + 1
					flag1,flag2,flag3,flag4,flag5=0,0,0,0,0
					while b< len(k) :
						 
						try:
							tags = tagger.tag_text(lemmatizer.lemmatize(k[b][0]))
							tag = treetaggerwrapper.make_tags(tags)
							tag_for_b = tag[0][1]

							#tag_for_b = word_pos_dict[lemmatizer.lemmatize(k[b][0])]
						except:
							tag_for_b = k[b][1]


						if (tag_for_b == 'NN' or tag_for_b == 'NNS' or tag_for_b == 'NNP' or tag_for_b == 'NNPS') and k[b][0] not in not_required:
							
							p = b
							word = lemmatizer.lemmatize(k[p][0])
							try:
								tags = tagger.tag_text(lemmatizer.lemmatize(k[p][0]))
								tag = treetaggerwrapper.make_tags(tags)
								tag_for_p = tag[0][1]
							except:
								tag_for_p = k[p][1]


							while p< len(k) and (tag_for_p == 'NN' or tag_for_p == 'NNS' or tag_for_p == 'NNP' or tag_for_p == 'NNPS'):
								p += 1
								if p < len(k):
									word = lemmatizer.lemmatize(k[p][0])
									try:
										tags = tagger.tag_text(lemmatizer.lemmatize(k[p][0]))
										tag = treetaggerwrapper.make_tags(tags)
										tag_for_p = tag[0][1]
										
									except:
										tag_for_p = k[p][1]
										 
									
									
								
								
							p -= 1
							try:
									tags = tagger.tag_text(lemmatizer.lemmatize(k[p][0]))
									tag = treetaggerwrapper.make_tags(tags)
									tag_for_p = tag[0][1]
									
							except:
									tag_for_p = k[p][1]
								
							k[p][0] = lemmatizer.lemmatize(k[p][0])
							print("1",i,k[p][0] ,tag_for_p, end = ' ')
							flag1=1
							if k[p][0] in feature_list :
								x = opinion_list_with_keys[i]
								y = feature_list_with_keys[k[p][0]]
								modification_mat[x][y] += 1					
							else:
								feature_list_with_keys[k[p][0]]	= count_features
								count_features += 1
								x = opinion_list_with_keys[i]
								y = feature_list_with_keys[k[p][0]]

								new_column = np.zeros((count_opinions,1) , dtype = int)

								modification_mat = np.append(modification_mat,new_column,axis = 1)
								modification_mat[x][y] += 1

							
							if p < (len(k)-2):
								p += 1
								try:
									tags = tagger.tag_text(lemmatizer.lemmatize(k[p][0]))
									tag = treetaggerwrapper.make_tags(tags)
									tag_for_p = tag[0][1]
								except:
									tag_for_p = k[p][1]

								
								if (tag_for_p == 'CC' or tag_for_p == ',' ):
									p += 1
									word = lemmatizer.lemmatize(k[p][0])
									try:
										tags = tagger.tag_text(lemmatizer.lemmatize(k[p][0]))
										tag = treetaggerwrapper.make_tags(tags)
										tag_for_p = tag[0][1]
									except:
										tag_for_p = k[p][1]

									

									while p< len(k) and (tag_for_p == 'NN' or tag_for_p == 'NNS' or tag_for_p == 'NNP' or tag_for_p == 'NNPS'):
										
										word = lemmatizer.lemmatize(k[p][0])
										try:
											tags = tagger.tag_text(lemmatizer.lemmatize(k[p][0]))
											tag = treetaggerwrapper.make_tags(tags)
											tag_for_p = tag[0][1]
										except:
											tag_for_p = k[p][1]

										p += 1 
										
									p -= 1
									try:
										tags = tagger.tag_text(lemmatizer.lemmatize(k[p][0]))
										tag = treetaggerwrapper.make_tags(tags)
										tag_for_p = tag[0][1]
										
									except:
										tag_for_p = k[p][1]
										
									k[p][0] = lemmatizer.lemmatize(k[p][0])
									print("2",i,k[p][0] ,tag_for_p, end = ' ')
									flag2=1

									if k[p][0] in feature_list :
										x = opinion_list_with_keys[i]
										y = feature_list_with_keys[k[p][0]]
										modification_mat[x][y] += 1					
									else:
										feature_list_with_keys[k[p][0]]	= count_features
										count_features += 1
										x = opinion_list_with_keys[i]
										y = feature_list_with_keys[k[p][0]]

										new_column = np.zeros((count_opinions,1) , dtype = int)

										modification_mat = np.append(modification_mat,new_column,axis = 1)
										modification_mat[x][y] += 1
			
									if p < (len(k)-2):
										p += 1
										try:
											tags = tagger.tag_text(lemmatizer.lemmatize(k[p][0]))
											tag = treetaggerwrapper.make_tags(tags)
											tag_for_p = tag[0][1]
										except:
											tag_for_p = k[p][1]


										if (tag_for_p == 'CC' or tag_for_p == ',' ):
											p += 1
											word = lemmatizer.lemmatize(k[p][0])
											try:
												tags = tagger.tag_text(lemmatizer.lemmatize(k[p][0]))
												tag = treetaggerwrapper.make_tags(tags)
												tag_for_p = tag[0][1]
											except:
												tag_for_p = k[p][1]

											

											while p< len(k) and (tag_for_p == 'NN' or tag_for_p == 'NNS' or tag_for_p == 'NNP' or tag_for_p == 'NNPS'):
												
												word = lemmatizer.lemmatize(k[p][0])
												try:
													tags = tagger.tag_text(lemmatizer.lemmatize(k[p][0]))
													tag = treetaggerwrapper.make_tags(tags)
													tag_for_p = tag[0][1]
												except:
													tag_for_p = k[p][1]
												p += 1 
												
											p -= 1
											try:
												tags = tagger.tag_text(lemmatizer.lemmatize(k[p][0]))
												tag = treetaggerwrapper.make_tags(tags)
												tag_for_p = tag[0][1]
									
											except:
												tag_for_p = k[p][1]
	
											k[p][0] = lemmatizer.lemmatize(k[p][0])
											print("3",i,k[p][0],tag_for_p , end = ' ')		
											flag3 =1
											if k[p][0] in feature_list :
												x = opinion_list_with_keys[i]
												y = feature_list_with_keys[k[p][0]]
												modification_mat[x][y] += 1					
											else:
												feature_list_with_keys[k[p][0]]	= count_features
												count_features += 1
												x = opinion_list_with_keys[i]
												y = feature_list_with_keys[k[p][0]]

												new_column = np.zeros((count_opinions,1) , dtype = int)

												modification_mat = np.append(modification_mat,new_column,axis = 1)
												modification_mat[x][y] += 1

								else :
										pass


							b = p + 1 


						elif (tag_for_b == 'JJ' or tag_for_b == 'JJS' or tag_for_b == 'JJS' or tag_for_b == 'RB' or tag_for_b == 'RBS' or tag_for_b == 'RBR' or tag_for_b == 'CC' or tag_for_b == ',' ) and k[b][0] not in not_required:
							p = b
							word = lemmatizer.lemmatize(k[p][0])
							try:
										tags = tagger.tag_text(lemmatizer.lemmatize(k[p][0]))
										tag = treetaggerwrapper.make_tags(tags)
										tag_for_p = tag[0][1]
							except:
								tag_for_p = k[p][1]


							while p< len(k) and (tag_for_p == 'JJ' or tag_for_p == 'JJS' or tag_for_p == 'JJS' or tag_for_p == 'RB' or tag_for_p == 'RBS' or tag_for_p == 'RBR' or tag_for_p == 'CC' or tag_for_p == ','):
								word = lemmatizer.lemmatize(k[p][0])
								try:
										tags = tagger.tag_text(lemmatizer.lemmatize(k[p][0]))
										tag = treetaggerwrapper.make_tags(tags)
										tag_for_p = tag[0][1]
								except:
									tag_for_p = k[p][1]
								p += 1
							
							if p < len(k):
								try:
										tags = tagger.tag_text(lemmatizer.lemmatize(k[p][0]))
										tag = treetaggerwrapper.make_tags(tags)
										tag_for_p = tag[0][1]
								except:
									tag_for_p = k[p][1]


								if (tag_for_p == 'NN' or tag_for_p == 'NNS' or tag_for_p == 'NNP' or tag_for_p == 'NNPS') and k[p][0] not in not_required:
									
									word = lemmatizer.lemmatize(k[p][0])
									

									while p< len(k) and (tag_for_p == 'NN' or tag_for_p == 'NNS' or tag_for_p == 'NNP' or tag_for_p == 'NNPS'):
										word = lemmatizer.lemmatize(k[p][0])
										try:
											tags = tagger.tag_text(lemmatizer.lemmatize(k[p][0]))
											tag = treetaggerwrapper.make_tags(tags)
											tag_for_p = tag[0][1]
										except:
											tag_for_p = k[p][1]

										p += 1								
								
								p -= 1
								k[p][0] = lemmatizer.lemmatize(k[p][0])
								try:
										tags = tagger.tag_text(lemmatizer.lemmatize(k[p][0]))
										tag = treetaggerwrapper.make_tags(tags)
										tag_for_p = tag[0][1]
									
								except:
									tag_for_p = k[p][1]
							
								print("4",i,k[p][0] ,tag_for_p, end = ' ')
								flag4 = 1
								if k[p][0] in  feature_list :
									x = opinion_list_with_keys[i]
									y = feature_list_with_keys[k[p][0]]
									modification_mat[x][y] += 1					
								
								else:
									feature_list_with_keys[k[p][0]]	= count_features
									count_features += 1
									x = opinion_list_with_keys[i]
									y = feature_list_with_keys[k[p][0]]

									new_column = np.zeros((count_opinions,1) , dtype = int)

									modification_mat = np.append(modification_mat,new_column,axis = 1)
									modification_mat[x][y] += 1

								
							if p < (len(k)-2):
								p += 1
								try:
										tags = tagger.tag_text(lemmatizer.lemmatize(k[p][0]))
										tag = treetaggerwrapper.make_tags(tags)
										tag_for_p = tag[0][1]
								except:
									tag_for_p = k[p][1]


								if (tag_for_p == 'CC' or tag_for_p == ',' ):
									p += 1

									word = lemmatizer.lemmatize(k[p][0])
									try:
										tags = tagger.tag_text(lemmatizer.lemmatize(k[p][0]))
										tag = treetaggerwrapper.make_tags(tags)
										tag_for_p = tag[0][1]
									except:
										tag_for_p = k[p][1]

									
									while p< len(k) and (tag_for_p == 'NN' or tag_for_p == 'NNS' or tag_for_p == 'NNP' or tag_for_p == 'NNPS'):
										word = lemmatizer.lemmatize(k[p][0])
										try:
											tags = tagger.tag_text(lemmatizer.lemmatize(k[p][0]))
											tag = treetaggerwrapper.make_tags(tags)
											tag_for_p = tag[0][1]
										except:
											tag_for_p = k[p][1]
										p += 1
										
									p -= 1
										
									k[p][0] = lemmatizer.lemmatize(k[p][0])
									try:
										tags = tagger.tag_text(lemmatizer.lemmatize(k[p][0]))
										tag = treetaggerwrapper.make_tags(tags)
										tag_for_p = tag[0][1]
									
									except:
										tag_for_p = k[p][1]

									print("5",i,k[p][0] ,tag_for_p, end = ' ')
									flag5 = 1
									if k[p][0] in feature_list :
										x = opinion_list_with_keys[i]
										y = feature_list_with_keys[k[p][0]]
										modification_mat[x][y] += 1					
									else:
										feature_list_with_keys[k[p][0]]	= count_features
										count_features += 1
										x = opinion_list_with_keys[i]
										y = feature_list_with_keys[k[p][0]]

										new_column = np.zeros((count_opinions,1) , dtype = int)

										modification_mat = np.append(modification_mat,new_column,axis = 1)
										modification_mat[x][y] += 1


					
				
							
							b = p + 1

						
						b += 1

					if flag1 == 0 and flag2 == 0 and flag3 == 0 and flag4 == 0 and flag5 == 0 :
						b = idx3 - 1
						while b >= 0 and flag4 == 0:
							try:
										tags = tagger.tag_text(lemmatizer.lemmatize(k[b][0]))
										tag = treetaggerwrapper.make_tags(tags)
										tag_for_b = tag[0][1]
							except:
								tag_for_b = k[b][1]

							if (tag_for_b == 'NN' or tag_for_b == 'NNS' or tag_for_b == 'NNP' or tag_for_b == 'NNPS') and k[b][0] not in not_required:
								flag4 = 1
								print("6",i,k[b][0] ,tag_for_b, end = ' ')
								if k[b][0] in feature_list :
										x = opinion_list_with_keys[i]
										y = feature_list_with_keys[k[b][0]]
										modification_mat[x][y] += 1					
								else:
										feature_list_with_keys[k[b][0]]	= count_features
										count_features += 1
										x = opinion_list_with_keys[i]
										y = feature_list_with_keys[k[b][0]]

										new_column = np.zeros((count_opinions,1) , dtype = int)

										modification_mat = np.append(modification_mat,new_column,axis = 1)
										modification_mat[x][y] += 1


							b -= 1				






	print('\n')	

index_to_be_removed =[]
index_to_be_retained =[]
for i in feature_list_with_keys:
	try :
		tags = tagger.tag_text(lemmatizer.lemmatize(k[p][0]))
		tag = treetaggerwrapper.make_tags(tags)
		tag = tag[0][1]	

	except:
		tag = pos_tag([i])[0][1]

	if 	tag != 'NN' and tag != 'NNPS' and tag != 'NNP' and tag != 'NNS':
		index_to_be_removed.append(feature_list_with_keys[i])
		#print( i , tag ,feature_list_with_keys[i])

	else:
		index_to_be_retained.append(feature_list_with_keys[i])
			

#print("remove" , index_to_be_removed)									

modification_mat = modification_mat[: , index_to_be_retained ]

new_feature_list_with_keys = {}

for idx,i in enumerate(index_to_be_retained):
		value = str(list(feature_list_with_keys.keys())[list(feature_list_with_keys.values()).index(i)])
		new_feature_list_with_keys[value] = idx 

print(new_feature_list_with_keys.keys())		
			
with open('modification_mat_part_1.pickle','wb') as h:
	pickle.dump(modification_mat,h)	

with open('feature_list_with_keys_part_1.pickle','wb') as h:
	pickle.dump(new_feature_list_with_keys,h)

f=open('modification_mat_part1_.txt','w')
for i in modification_mat:
	for j in i:
		a= str(j) + " "	
		f.write(a)
	f.write('\n')

f.close()

	
	
