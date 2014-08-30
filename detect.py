import math
from nltk.tokenize import *
from nltk.probability import *


def main():
	THRESHOLD = -400
	docs = 95
	
	d_file = open('dictionary2').readlines()
	dict_key = []
	dict_occ = []
	dict_indx = []
	
	test_file = open('test', 'w')
	test_file.write('0 ')				#Writing label 0
	
	i = 0
	for line in d_file:
		tmp = line.strip()
		tmp = tmp.split()
		dict_indx.append(i)
		dict_key.append(tmp[0])
		dict_occ.append(int(tmp[1]))
		i=i+1
		
	fin = open('newmail','r').read().lower()
	tokenizer = RegexpTokenizer('[\w\.]+(@)[\w\.]+|[\w]*(http)[s]?[^"<>\s]+|\w+')
	words2 = tokenizer.tokenize(fin)
	words = []
	
	for it in words2:
		if len(it)>2:
			words.append(it)
	
	fdist = FreqDist(words)
	
	f_out = open('test_idf.db', 'w')

	j=0
	for it in dict_key:
		if it in fdist.keys():
			tmp = 0.5*(0.5+ float(fdist[it])/float(fdist[fdist.max()]))*math.log(float(docs)/float((dict_occ[j]+1)), 2)
			f_out.write(it+" "+str(tmp)+'\n')
			if tmp>THRESHOLD:
				test_file.write(str(dict_indx[j])+":"+str(tmp)+" ")
		j = j+1		
		
	f_out.close()
		
	test_file.close()
			
if __name__=='__main__':
	main()
