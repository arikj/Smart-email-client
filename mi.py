#Mutual Information

from nltk.tokenize import *
from nltk.probability import *
import math
import collections


def sort_count(x):
	counter = collections.Counter(x)
	X = []
	Y = []
	for (y,x) in sorted(zip(counter.values(),counter.keys()), reverse=True):
		X.append(x)
		Y.append(y)
	return zip(X,Y)
	
	

def main():
	SMOOTHENING = 0.5
	ran = range(3)
	
	#Tokenization
	inp = open("newmail", "r").read().lower()
	
	tokenizer = RegexpTokenizer('[\w\.]+(@)[\w\.]+|[\w]*(http)[s]?[^"<>\s]+|\w+')
	words = tokenizer.tokenize(inp)
	
	fdist = FreqDist(words)
	
	f_out = open("test_words.db", "w")
	for it in fdist.items():
		f_out.write(it[0]+' '+str(it[1])+'\n')
	
	li = []
	for i in ran:
		path = 'class'+str(i)+'/'
		
		freq_file = open(path+'rel_word.db').readlines()

		for line in freq_file:
			tmp = line.strip()
			tmp = tmp.split()
			for it in range(int(tmp[1])):
				li.append(tmp[0])
	
	li = sort_count(li)
	dict_key = []
	dict_freq = []

	grand_total = 0.0
	for it in li:
		dict_key.append(it[0])
		dict_freq.append(it[1])
		grand_total += it[1]
		
	#calculating pl
	pl = []
	for it in fdist.keys():
		if it in dict_key:
			pl.append(float(dict_freq[dict_key.index(it)])/grand_total)
		else:
			pl.append(1.0)

	
	pc = 1/float(len(ran))		#Prob of a given class
	
	for i in ran:
		path = 'class'+str(i)+'/'
		
		freq_file = open(path+'rel_word.db').readlines()
		freq = []
		key = []

		total_count = 0
		for line in freq_file:
			tmp = line.strip()
			tmp = tmp.split()
			key.append(tmp[0])
			freq.append(float(tmp[1]))
			total_count += float(tmp[1])
		
		j=0
		mi = 0
		for it in fdist.keys():
			if it in key:
				n = freq[key.index(it)]
			else:
				n = 0
				
			cp = (n+SMOOTHENING)/(total_count+len(key)*SMOOTHENING)
			if pl[j]!=1:
				mi = mi+ math.log( abs((cp * math.log(cp/(pc*pl[j])))), 2)
			j=j+1
			
		print i, mi
		
		
			
if __name__=='__main__':
	main()
