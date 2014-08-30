#Conditional Probability

from nltk.tokenize import *
from nltk.probability import *
import math


def main():
	SMOOTHENING = 0.5
	ran = range(3)
	
	#Tokenization
	inp = open("newmail", "r").read().lower()
	
	tokenizer = RegexpTokenizer('[\w\.]+(@)[\w\.]+|[\w]*(http)[s]?[^"<>\s]+|\w+')
	words = tokenizer.tokenize(inp)
	
	fdist = FreqDist(words)
	
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
		
		prob = 1.0
		for it in fdist.keys():
			if it in key:
				n = freq[key.index(it)]
			else:
				n = 0
			prob = prob + math.log((n+SMOOTHENING)/(total_count+len(key)*SMOOTHENING))
			
		print i,prob
		
		
			
if __name__=='__main__':
	main()
