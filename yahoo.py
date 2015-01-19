from query import *
import imaplib
import re
import sys
import urllib2,urllib
from HTMLParser import HTMLParser
import urlparse
from urlparse import urljoin
import json
import email
import nltk
import time
import os,os.path
import shutil

pattern_uid = re.compile('\d+ \(UID (?P<uid>\d+)\)')

num_folders = 4
maxi = 20
mail_header={}
folders=[]
def extract_body(payload):
    if isinstance(payload,str):
        return payload
    else:
        return '\n'.join([extract_body(part.get_payload()) for part in payload])

sys.stderr = sys.stdout


def parse_uid(data):
    match = pattern_uid.match(data)
    return match.group('uid')
    
    
#setting proxy connection
proxy = urllib2.ProxyHandler({'https': 'http://password:username@ironport2.iitk.ac.in:3128',
			      'http': 'http://password:username@ironport2.iitk.ac.in:3128'})
auth = urllib2.HTTPBasicAuthHandler()
opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler,urllib2.HTTPSHandler,urllib2.HTTPRedirectHandler)
urllib2.install_opener(opener)
#proxy connection made

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('username@gmail.com', 'password')

#folders = [folder.split(' "/" ')[1][1:-1] for folder in mail.list()[1]]	
folders = ["Inbox", "antaragni", "technology", "spo", "sports"]
#for j in range(0,len(folders)):
#	print folders[j]
	
# Out: list of "folders" aka labels in gmail.

def start_func():
	
	
	mail.select("Inbox") # connect to inbox.
	result, data = mail.search(None,'(UNSEEN)')

	ids = data[0]						 # data is a list.
	id_list = ids.split()		 # ids is a space separated string
	i=0;
	
	
	
	for fold in range(1,num_folders):
		path, dirs, files = os.walk('class_new'+str(fold)).next()
		count=0
		for i in files:
			if 'inbox' not in i.lower():
				count+=1 
		nfiles=count/2
		#nfiles = len(os.listdir('class_new'+str(fold)))/2
		#print nfiles
		mail_header[folders[fold]]=[]
		for i in range(0,nfiles):
			filename = str(folders[fold])+"_header"+str(i+1)
			try:
				f=open('class_new'+str(fold)+'/'+filename,'r').readlines()
				data_body = []
				for line in f:
					data_body.append(line)
				mail_header[folders[fold]].append(data_body)
			except:
				pass

	mail_header["Inbox"]=[]
	i=0;
	for email_id in id_list:
		i=i+1
	
		#mail.store(email_id, '+FLAGS', '\\UnSeen')  #to tag the read mail as seen..
		result_uid,data_uid = mail.fetch(email_id, "(UID)")
		try:
			msg_uid = parse_uid(data_uid[0])
		except:
			pass
		
		result_mail,data_mail = mail.fetch(email_id, "(RFC822)");
		raw_email = data_mail[0][1] # here's the body, which is raw text of the whole email
		
		email_message = email.message_from_string(raw_email)
		receiver = email_message['To']
		subject = email_message['Subject']
		sender = email.utils.parseaddr(email_message['From'])
		
		payload=email_message.get_payload()
		body = extract_body(payload)
		
		if email_message.get_content_type() == "multipart/mixed":
			continue
		
		elif email_message.get_content_type() == "text/html":
			body = nltk.clean_html(body)	

		indx1 = body.find("html")
		indx2 = body.find("<p>")
		
		if indx1!=-1 and indx2!=-1:
			if indx1<indx2:
				body = body[ :indx1]
			else:
				body = body[ :indx2]
				
		elif indx1!=-1:
			body = body[ :indx1]
		
		elif indx2!=-1:
			body = body[ :indx2]
			
		file1 = "Inbox"+str(i);	
		#var="Receiver: "+str(receiver) +"\nSender: "+str(sender)+"\nSubject:"+str(subject)+"\nBody: "+str(body);
		info = str(sender)+"          "+str(subject)
		try:
			mail_header["Inbox"].append(info)
		except:
			pass
		
		
		f2 = open('class_new0/'+file1,'w')
		f2.write(body)
		f2.close()
	
		file_send = open("check",'w')
		file_send.write(str(info) +"\n"+ str(body))
		file_send.close()
		return_index = query(open("check").read())
		path, dirs, files = os.walk('class_new'+str(return_index)).next()
		count=0
		for j in files:
			if 'inbox' not in j.lower():
				count+=1 
		nfiles=count/2+1
		if return_index!=0:
			shutil.move("class_new0/file1","class_new"+str(return_index)+"/"+folders[return_index]+nfiles);
			file_send = open("class_new"+str(return_index)+"/"+folders[return_index]+"_header"+nfiles,'w')
			file_send.write(str(info))
			file_send.close()
			mail_header["Inbox"].pop()
			file_send = open("class_"+str(return_index)+"/"+"file"+nfiles,'w')
			file_send.write(str(info)+"\n"+ str(body))
			file_send.close()
			
		result = mail.uid('COPY', msg_uid, folders[return_index])
		if result[0] == 'OK':
			mov_del, data_del = mail.uid('STORE', msg_uid , '+FLAGS', '(\Deleted)')
			mail.expunge()

start_func()
		
