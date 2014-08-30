import os
from collections import Counter
from collections import OrderedDict
import nltk
from nltk.tokenize import *
from nltk.probability import *


def main():			
	ran = range(3)

	d_file = open('dictionary').readlines()
	d_out = open('dictionary','w')
	dict_key = []
	dict_occ = []
	
	for line in d_file:
		tmp = line.strip()
		tmp = tmp.split()
		dict_key.append(tmp[0])
		dict_occ.append(int(tmp[1]))


	for labl in ran:
		path = 'class'+str(labl)+'/'
		
		freq_file = open(path+'word.db').readlines()
		freq = []
		key = []

		for line in freq_file:
			tmp = line.strip()
			tmp = tmp.split()
			key.append(tmp[0])
			freq.append(int(tmp[1]))
		
		files =  os.listdir(path)
		for f in files:
			if os.path.isdir(f) == False and "file" in f :
				fin = open(path+f,'r').read().lower()
				tokenizer = RegexpTokenizer('[\w\.]+(@)[\w\.]+|[\w]*(http)[s]?[^"<>\s]+|\w+')
				words2 = tokenizer.tokenize(fin)
				words = []
				
				for it in words2:
					if len(it)>2:
						words.append(it)
						
				for it in words:
					if it in key:
						freq[key.index(it)] += 1
					else:
						key.append(it)
						freq.append(1)
		
		fout = open(path+'word.db','w')
		
		i=0
		for it in key:
			fout.write(it+' '+str(freq[i])+'\n')
			i=i+1
		
		for it in key:
			if it in dict_key:
				dict_occ[dict_key.index(it)] += 1
			else:
				dict_key.append(it)
				dict_occ.append(1)
		
		fout.close()
	
	i=0
	for it in dict_key:
		d_out.write(it+' '+str(dict_occ[i])+'\n')
		i=i+1
		
	d_out.close()
        
if __name__=='__main__':
	main()
