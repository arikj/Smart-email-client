
def main():
	ran = range(3)
	
	for i in ran:
		
		path = 'class'+str(i)+'/'
			
		f = open(path+'word.db','w')
		f.close()
		
	f = open('dictionary','w')
	f.close()
	
	f = open('dictionary2','w')
	f.close()

if __name__=='__main__':
	main()
