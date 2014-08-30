#Inverse document frequency example

from nltk.tokenize import * 
	
def tkn():
	
	#Tokenization
	#inp = open("newmail.txt", "r").read()
	
	inp = '<ko.ko_ko@gmail.co.in.ji>) this is bhav. time = 212121.93i232'
	tokenizer = RegexpTokenizer('[\w\.]+(@)[\w\.]+|[\w\.]*(http)[s]?[\w\.]+|\w+')
	print tokenizer.tokenize(inp)

tkn()
