import os
from collections import Counter
from collections import OrderedDict
import nltk
from nltk.tokenize import *
from nltk.probability import *
import math


def main():			
	ran = range(3)
	docs = 94
	
	f_out = open('training','w')
	
	d_file = open('dictionary2').readlines()
	dict_key = []
	dict_occ = []
	dict_indx = []
	
	i = 0
	for line in d_file:
		tmp = line.strip()
		tmp = tmp.split()
		dict_indx.append(i)
		dict_key.append(tmp[0])
		dict_occ.append(int(tmp[1]))
		i=i+1
	
	
	for labl in ran:
		path = 'class'+str(labl)+'/'
		
		for files in os.listdir(path):
			if "file" in files:
				inp = open(path+files).read().lower()
			
				tokenizer = RegexpTokenizer('[\w\.]+(@)[\w\.]+|[\w]*(http)[s]?[^"<>\s]+|\w+')
				words = tokenizer.tokenize(inp)
	
				fdist = FreqDist(words)
				
				j=0
				f_out.write(str(labl+1))
				for it in dict_key:
					if it in fdist.keys():
						ifd = 0.5*(0.5+float(fdist[it])/fdist[fdist.max()])*math.log(float(docs)/float(dict_occ[j]), 2)
						f_out.write(" "+str(j)+":"+str(ifd))
					j=j+1
				f_out.write('\n')
				
	
if __name__=='__main__':
	main()
