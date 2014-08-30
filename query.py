
import math
import os
from nltk.tokenize import *
from nltk.probability import *
import collections


def sort_count(x):
	counter = collections.Counter(x)
	X = []
	Y = []
	for (y,x) in sorted(zip(counter.values(),counter.keys()), reverse=True):
		X.append(x)
		Y.append(y)
	return zip(X,Y)
	
	

def query(inp):
	ran = range(3)
	
	SMOOTHENING = 0.5
	THRESHOLD = 85.0
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
		
	tokenizer = RegexpTokenizer('[\w\.]+(@)[\w\.]+|[\w]*(http)[s]?[^"<>\s]+|\w+')
	words2 = tokenizer.tokenize(inp)
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
			test_file.write(str(dict_indx[j])+":"+str(tmp)+" ")
		j = j+1		
		
	f_out.close()

	test_file.close()

	os.system('./svm.sh')
	
	print "Classified using SVM"
	
	ans = open('answer').readlines()
	ans = ans[1].split()
	
	folder = 0
	
	if float(ans[int(float(ans[0]))])>THRESHOLD:
		folder = int(float(ans[0]))
		
	#return folder
	
	#Mutual information
	
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
	
	max_mi = -100000
	gmi = []
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
		
		gmi.append(mi)
		if mi>max_mi:
			max_mi = mi	

	print "Classified using MI"
	
	if folder == 0:
		return folder
	elif gmi[folder-1]==max_mi:
		return folder
	else:
		return 0
	
	

if __name__=='__main__':
	main(open('newmail').read())

