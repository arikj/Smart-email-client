import os
from collections import Counter
from collections import OrderedDict
import nltk
from nltk.tokenize import *
from nltk.probability import *


def main():			
	ran = range(3)

	d_file = open('dictionary2').readlines()
	dict_key = []
	dict_occ = []
	
	for line in d_file:
		tmp = line.strip()
		tmp = tmp.split()
		dict_key.append(tmp[0])
		dict_occ.append(int(tmp[1]))
		
	d = open('dictionary2', 'w')
	docs = 0
	
	for labl in ran:
		path = 'class'+str(labl)+'/'
		
		for files in os.listdir(path):
			if "file" in files:
				inp = open(path+files).read().lower()
			
				tokenizer = RegexpTokenizer('[\w\.]+(@)[\w\.]+|[\w]*(http)[s]?[^"<>\s]+|\w+')
				words = tokenizer.tokenize(inp)
	
				fdist = FreqDist(words)
				
				for it in fdist.keys():
					if it in dict_key:
						dict_occ[dict_key.index(it)] += 1
					else:
						dict_key.append(it)
						dict_occ.append(1)
				docs = docs+1
	
	i=0
	for it in dict_key:
		d.write(it+' '+str(dict_occ[i])+'\n')
		i = i+1
	
	print "Total no. of Documents = "+str(docs)
	
if __name__=='__main__':
	main()
