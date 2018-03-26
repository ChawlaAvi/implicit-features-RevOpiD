from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import word_tokenize, pos_tag
import string, re
from autocorrect import spell
from nltk.tokenize import TweetTokenizer
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import state_union
import nltk
import pickle
import treetaggerwrapper


tagger = treetaggerwrapper.TreeTagger(TAGLANG='en')
punct = set(string.punctuation)
lancaster_stemmer = LancasterStemmer()
tknzr = TweetTokenizer()  # This helps maintain apostrophe like "hasn't"
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

with open('cleandata1_pos.pickle','rb') as h:
	word_pos_dict=pickle.load(h)






r = []
f = open('cleandata1.txt', 'r')

for l in f:
	r.append(l[:-1])
f.close()



chunkList = []
for idx,r1 in enumerate(r):

	r2 = r1.lower()
	for r3 in r2.split('.'):
		r3 = tknzr.tokenize(r1)    # or word_tokenize(r1) tknzr.tokenize   to be checked whether it'll be r1 or r3
		tagged =[]
		for i in r3:
				#if pos_tag([i]) == 'NNS' or pos_tag([i]) == 'NNP' or pos_tag([i]) == 'NN' or pos_tag([i]) == 'NNPS' or pos_tag([i]) == 'JJ' or pos_tag([i]) == 'JJS' or pos_tag([i]) == 'JJR' :
					try:
						#tag = word_pos_dict[i]
						tags = tagger.tag_text(i)
						tag = treetaggerwrapper.make_tags(tags)
						tag = tag[0][1]


					except:
						tag = pos_tag([i])[0][1]

					avi =[]
					avi.append(i)
					avi.append(tag)

					tagged.append(tuple(avi))


				# else:
				# 	tag =pos_tag([i])[0][1]
				# 	avi =[]
				# 	avi.append(i)
				# 	avi.append(tag)

				# 	tagged.append(tuple(avi))

		
		chunkGram = "NP: {<DT>?<JJ>+<NN>}"
		chunkParser = nltk.RegexpParser(chunkGram)

		chunked = chunkParser.parse(tagged)
		chunkList.append(chunked)


'''
for i in chunkList[0:5]:
	for sub in i.subtrees():
		print(sub.leaves())
'''
noun_phrase_list = []
for i in chunkList:
	for subtree in i.subtrees():
			if subtree.label() == 'NP':
				np_phrase = []
				for idx, x in enumerate(subtree.leaves()):
					if (x[0] == '"' or x[0] in '\/'):
						continue
					np_phrase.append(x[0])
				noun_phrase_list.append(np_phrase)



#print("\n \n \n \n",noun_phrase_list[0:10])

f = open('noun_phrase2.txt', 'w')


for i in noun_phrase_list:
	f.write(' '.join(i))
	f.write('\n')
f.close()
