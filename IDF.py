#Inverse document frequency

import math
import os

def main():
	THRESHOLD = 0.1
	ran = range(3)
	
	docs = len(ran)
	
	d_file = open('dictionary').readlines()
	dict_key = []
	dict_occ = []
	dict_indx = []
	
	train_file = open('training', 'w')
	
	i = 0
	for line in d_file:
		tmp = line.strip()
		tmp = tmp.split()
		dict_indx.append(i)
		dict_key.append(tmp[0])
		dict_occ.append(int(tmp[1]))
		i=i+1
		
		
	for i in ran:
		train_file.write(str(i+1))
		
		path = 'class'+str(i)+'/'
		
		freq_file = open(path+'word.db').readlines()
		freq = []
		key = []

		maximum = 0
		for line in freq_file:
			tmp = line.strip()
			tmp = tmp.split()
			key.append(tmp[0])
			freq.append(int(tmp[1]))
			if maximum<int(tmp[1]):
				maximum = int(tmp[1])
		
		f_out = open(path+'idf.db', 'w')
		f_out2 = open(path+'rel_word.db', 'w')
		
		j=0
		for it in dict_key:
			if it in key:
				indx = key.index(it)
				tmp = 0.5*(0.5+float(freq[indx])/float(maximum))*math.log(float(docs)/float(dict_occ[j]), 2)
				f_out.write(it+" "+str(tmp)+'\n')
				if tmp>THRESHOLD:
					train_file.write(" "+str(dict_indx[j])+":"+str(tmp))
					f_out2.write(it+" "+str(freq[indx])+'\n')
			j = j+1		
		
		f_out.close()
		f_out2.close()
		
		train_file.write('\n')
		
	train_file.close()
			
if __name__=='__main__':
	main()
