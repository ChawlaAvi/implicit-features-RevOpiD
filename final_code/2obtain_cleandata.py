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

punct = set(string.punctuation)
lancaster_stemmer = LancasterStemmer()
tknzr = TweetTokenizer()  # This helps maintain apostrophe like "hasn't"
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

with open('cleandata1_pos.pickle','rb') as h:
	word_pos_dict=pickle.load(h)

with open("tokenized_sentences.pickle",'rb') as h:
		 r= pickle.load(h)



iwtk=["and","not","but","against","below","no","nor","same","hasnt","couldnt","unable","wouldnt","wasnt","werent","wont","isnt"
,"shouldnt","mustn","wouldn","shouldn","haven","doesn","couldn","weren","hasn","aren","wasn"]

to_be_modified=["mustn","wouldn","shouldn","haven","doesn","couldn","weren","hasn","aren","wasn"]

RE_D = re.compile('\d')
RE_AP = re.compile("'")
RE_DO = re.compile("\.")

limit = 0
i = 0
'''
f=open('hotel_218524.dat','r')
r=[]

for i in f:
	if re.match("<Content>.*", i) and len(i)>150:
		temp=str(i[9:len(i)-2])
		temp=''.join(x for x in temp)
		r.append(temp)



'''

for idx,i in enumerate(r):
	p = ''
	for j in i:
		p = p + j

	r[idx] = p
	


for i in range(len(r)):
	r[i]=r[i].lower()
	r[i]=r[i].replace("!",".")
	
	r[i] = re.sub(r'\.+', ".", r[i])
	r[i] = r[i].replace(","," , ")
	r[i] = r[i].replace(";"," ; ")
	r[i] = r[i].replace(":"," : ")
	r[i] = r[i].replace("?"," . ")

	r[i] = r[i].replace("."," . ")
	r[i] = re.sub("\s\s+" , " ", r[i])
	


for i in range(len(r)):
	r[i]=r[i].lower()
	r[i]=r[i].split()
	for j in range(len(r[i])):
		if (r[i][j] in stop_words) and (r[i][j] not in iwtk):
			r[i][j] = ''

	
	
	r[i] = ' '.join((' '.join(r[i])).strip().split())    

for i in range(len(r)):
	r[i]=r[i].lower()
	r[i]=r[i].split()
	for j in range(len(r[i])):
		if (r[i][j] in to_be_modified):
			r[i][j] = r[i][j] + "t"

	
	
	r[i] = ' '.join((' '.join(r[i])).strip().split())    


'''
uptil this , i have all the the sentences with me in which all the stopwords
have been removed except those present in the list (iwtk) .


now we shall proceed for spell check.
'''

f=open('file1_before_lemmatize.txt','w')
for i in r:
	f.write(i)
	if i[-1] != '.' : 
		f.write(' .')
	f.write('\n')

f.close()
	

for i in range(len(r)):
	r[i]=r[i].split()
	for j in range(len(r[i])):
		if ((r[i][j] not in set(string.punctuation))) and (not (RE_D.search(r[i][j]))):	
			r[i][j] = spell(r[i][j])
		r[i][j] = lemmatizer.lemmatize(r[i][j],'v')

	r[i] = ' '.join(r[i])
	r[i] = re.sub('\s+', ' ', r[i])

f = open("cleandata1.txt",'w')
for i in r:
	f.write(i)
	if i[-1] != '.' : 
		f.write(' .')
	f.write('\n')

f.close()