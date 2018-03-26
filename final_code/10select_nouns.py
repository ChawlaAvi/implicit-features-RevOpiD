import pickle
import re
import string

from nltk import pos_tag
from nltk.corpus import stopwords
import treetaggerwrapper


tagger = treetaggerwrapper.TreeTagger(TAGLANG='en')
stop=set(stopwords.words('english'))
punc = set(string.punctuation)

#nouns_list = ['suction', 'mechanism', 'puller', 'grip', 'dent', 'diameter', 'cup', "it's", "i'm", 'cup', 'money', 'product', 'quality', 'work', 'size', 'job', 'item', 'rubber', 'tool', 'metal']

not_required = set(['not','it','its','''it's''' , 'and','''weren't''','''haven't''' , 'or','u','etc','''you're''','that','''that's''','okay','''don't''','dont','cant','''can't''','''i've''','oh','ohh','''we've''','have','we',
'were','could','''couldn't''','couldnt','you','didnt','''didn't''','did','does','doesnt', '''doesn't''','should','''shouldn't''','your',
'''yours''','''your's''','wont','''won't''','a','an','the','our','ours','''our's''','as','being','been','he','him','himself','she','her'
,'herself','only','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])

not_required = not_required | stop | punc

with open('positive_dict.pickle', 'rb') as handle:
    positive_dict = pickle.load(handle)

with open('negative_dict.pickle', 'rb') as handle:
    negative_dict = pickle.load(handle)

with open('neutral_dict.pickle', 'rb') as handle:
    neutral_dict = pickle.load(handle)

with open('cleandata1_pos.pickle','rb') as h:
	word_pos_dict=pickle.load(h)

with open('final_adjective_list.pickle','rb') as h:
	adj_list = pickle.load(h)


noun_list = []

for x in positive_dict:
	noun_list.append(x)
for x in negative_dict:
	noun_list.append(x)

noun_list = list(set(noun_list))

f = open('cleaned_data_for_pruning.txt', 'r')

sentences = []

for l in f:
	se = re.sub("[^\w\d'\s.]+",'',l)
	x = se.strip().split('.')
	for i in x:
		sentences.append(i.strip())
#print(sentences)

words_in_sentence = []
for i in range(len(sentences)):
	print("1 ->" , i ,len(sentences))
	if sentences[i] != '' or sentences[i] != '\n':
		sentence_word = sentences[i].split(' ')
		sentence_word = list(filter(None, sentence_word))
	if sentence_word != []:
		words_in_sentence.append(sentence_word)

f.close()
count_list = []
for idx,i in enumerate(noun_list):
	count = 0
	print(idx , len(noun_list))
	for sent in words_in_sentence:
		count += sent.count(i)
	count_list.append(count)

sorted_noun_list = [i[0] for i in sorted(zip(noun_list, count_list), key=lambda l: l[1], reverse=True)]
count2_simple = sorted(count_list, reverse=True)



count_to_be_selected = int(len(sorted_noun_list))

selected_nouns = set(sorted_noun_list[ : count_to_be_selected])

selected_nouns = selected_nouns - not_required

selected_nouns =[i for i in selected_nouns if len(i) >= 3] 
selected_nouns = list(selected_nouns)

#print(selected_nouns)
#quit()

#a = set(selected_nouns) & set(nouns_list)

'''
print("Precision:", len(a)/len(selected_nouns))
print("Recall:", len(a)/len(nouns_list))

for i in selected_nouns:
	print(i)'''

feature_list = []
feature_list_without_neutral = []
feature_list_without_one = []
feature_list_without_two = []


for idx,x in enumerate(positive_dict):
	print("positive",idx,len(positive_dict))
	if x in selected_nouns:

		
		print(x)
		print(positive_dict[x])
		print(len(positive_dict[x]))
		
		
		

for idx,x in enumerate(negative_dict):
	print("negative",idx,len(negative_dict))
	if x in selected_nouns:
		print(x)
		print(negative_dict[x])
		print(len(negative_dict[x]))
		

for idx,x in enumerate(neutral_dict):
	print("neutral",idx,len(neutral_dict))
	if x in selected_nouns:
		print(x)
		print(neutral_dict[x])
		print(len(neutral_dict[x]))
		
all_together ={}

for idx,x in enumerate(selected_nouns):
	print("all" , idx,len(selected_nouns))
	b=[]
	if x in positive_dict.keys():
		for i in positive_dict[x]:
			b.append(i[0][1][0])
	
	
	if x in negative_dict.keys():
		for i in negative_dict[x]:
			b.append(i[0][1][0])

	
	if x in neutral_dict.keys():
		for i in neutral_dict[x]:
			b.append(i[0][1][0])

		
	all_together[x] = list(set(b))
	

new_dict ={}
removed_dict ={}
for i in all_together.keys():
	#if (pos_tag([i])[0][1] == 'NN' or pos_tag([i])[0][1] == 'NNPS' or pos_tag([i])[0][1] == 'NNP' or pos_tag([i])[0][1] == 'NNS') and i not in adj_list:
	try:
		tags = tagger.tag_text(i)
		tag = treetaggerwrapper.make_tags(tags)
		tag = tag[0][1]
	except:
		tag = pos_tag([i])[0][1]
	if ( tag == 'NN' or tag == 'NNPS' or tag == 'NNP' or tag == 'NNS'):
		new_dict[i] = all_together[i]
	else:
		removed_dict[i] = all_together[i]


with open('removed_after_select_nouns.pickle','wb') as h:
	pickle.dump(removed_dict,h)

with open('all_feature_dict.pickle','wb') as h:
	pickle.dump(all_together,h)

with open('all_together_in_a_dict.pickle','wb') as h:
	pickle.dump( new_dict ,h)



