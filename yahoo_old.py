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

def extract_body(payload):
    if isinstance(payload,str):
        return payload
    else:
        return '\n'.join([extract_body(part.get_payload()) for part in payload])

sys.stderr = sys.stdout

#setting proxy connection
proxy = urllib2.ProxyHandler({'https': 'http://shahak:karan107@ironport2.iitk.ac.in:3128',
			      'http': 'http://shahak:karan107@ironport2.iitk.ac.in:3128'})
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
mail.login('bhavishya235@gmail.com', 'iitairtwo35')

mail.list()
# Out: list of "folders" aka labels in gmail.
mail.select("spo", readonly=True) # connect to inbox.
result, data = mail.search(None,'(ALL)')

ids = data[0]						 # data is a list.
id_list = ids.split()		 # ids is a space separated string
i=0;


for email_id in id_list:
	i=i+1;
	if i>20:
		break
	#mail.store(email_id, '+FLAGS', '\\UnSeen')  #to tag the read mail as seen..
	result_mail,data_mail = mail.fetch(email_id, "(RFC822)");

	raw_email = data_mail[0][1] # here's the body, which is raw text of the whole email
	
	email_message = email.message_from_string(raw_email)
	receiver = email_message['To']
	subject = email_message['Subject']
	sender = email.utils.parseaddr(email_message['From'])
	
	payload=email_message.get_payload()
	body = extract_body(payload)
	
	if email_message.get_content_type() == "text/html":
		body = nltk.clean_html(body)
	
	
	var="Receiver: "+receiver +"\nSender: "+str(sender)+"\nSubject:"+subject+"\nBody: "+body;
	file1 = "file"+str(i);
	f2 = open(file1,'w')
	f2.write(var)
	f2.close()
	


	
