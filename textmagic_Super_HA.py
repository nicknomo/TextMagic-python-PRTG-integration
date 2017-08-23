#This was written in Python 3
# Requires DNS PYTHON http://www.dnspython.org/
# Requires textmagic python library https://www.textmagic.com/docs/api/python/
### IMPORTANT - Set the PRTG timeout to at least 180 seconds so it can properly search for DNS ###
### IMPORTANT - Set the PRTG timeout to at least 180 seconds so it can properly search for DNS ###

import sys
import os
import dns.resolver

##### USER CONFIGURABLE SECTION #####
#### ALL VARIABLES MUST BE CHANGE! ####
##### USER CONFIGURABLE SECTION #####

#your username and API key are found on the textmagic site 
username = "usernamegoeshere"
apikey = "Rasd123sdfsdfscszxxzorsomething"

#for Text2speech, the recipient has to be a member of list
#On the textmagic Web UI contacts section to make a list and the contacts, set them manually to landline
#Go to the Web ui's services secion, go to text to speech, and set it to enabled for landline phones.
#Now go to the sandbox section and user GET /api/v2/lists/search . Hit sandbox, and then TRY. Your lists ids will be in there
#https://rest.textmagic.com/api/v2/doc#get--api-v2-lists-search
#Put the relevant list id into here
recipients='999999'


#This is the backup gateway ip if you have one
backupgwip = '192.168.1.2'
backupgwipv6 = 'fd00:0:0:1::2'

#This is the interface windows associates with your ipv6 backup gateway
#This could still be your default adapter, or maybe a secondary adapter
#When the primary attempt at your default ipv4 and ipv6 gateway fails, it tries this adapter
#To find the correct adapter USE:  netsh int ipv4 show interfaces    
# THE DEFAULT IS ALMOST CERTAINLY WRONG!!!!
ipv6intnum = '1'

### If ALL dns attempts fail, this will be what is passed to the socket
manualtextmagicipv4_1 = '104.20.24.237'
manualtextmagicipv4_2 = '104.20.23.237'
manualtextmagicipv6_1 = '2400:cb00:2048:1::6814:18ed'
manualtextmagicipv6_2 = '2400:cb00:2048:1::6814:17ed'

### These are BACKUP DNS providers in case your main dns provider fails
### It also is what the system will ping to attempt to check for internet connectivity
dnsprovider1 = '8.8.8.8'
dnsprovider2 = '8.8.4.4'
dnsprovider3 = '4.2.2.1'
dnsprovider1ipv6 = '2001:4860:4860::8888'
dnsprovider2ipv6 = '2001:4860:4860::8844'
#OpenNIC
dnsprovider3ipv6 = '2001:470:1f10:c6::2'


##### END OF USER CONFIGURABLE SECTION #####
##### END USER CONFIGURABLE SECTION #####



#the PRTG output is processed then repeated
#this allows the user to keep listening, since the text2speech can be spotty
args = sys.argv[1:]
arguments = ''.join(str(x)+' ' for x in args)
arguments = arguments+arguments


### This runs a dns query and returns a list of ip addresses
def rundnsquery(dnsrequest,host):	
	dnslist = []	
	
	try:
	    	answers = dnsrequest.query(host, 'A')
	    	for rdata in answers:
	    		dnsip = rdata.to_text()
	    		dnsentry = (2,1,0, '', (dnsip,443))
	    		dnslist.append(dnsentry)
	    	
	except BaseException as e:
		print(e)

	try:
		answers = dnsrequest.query(host, 'AAAA')
		for rdata in answers:
	    		dnsip = rdata.to_text()
	    		dnsentry = (23,1,0, '', (dnsip, 443, 0, 0))
	    		dnslist.append(dnsentry)

	except BaseException as e:
		print(e)	
		
	if (dnslist): 
		return dnslist
	else:
		return []
	

### This is what will return a list of dns results to make the request
### If no result is found, hardcoded ip's are used (found in the user configurable section
def getdnsip(host):
	
	dnsrequest = dns.resolver.Resolver()
	dnsrequest.timeout = 3
	dnsrequest.lifetime = 6
	dnslist = []	
	
	#first we try with the default windows dns settings
	dnslist = rundnsquery(dnsrequest,host)
	if (dnslist): return dnslist
    
	#now we try with different global providers
	dnsrequest.nameservers = [dnsprovider1]
	dnslist = rundnsquery(dnsrequest,host)
	if (dnslist): return dnslist

	dnsrequest.nameservers = [dnsprovider2]
	dnslist = rundnsquery(dnsrequest,host)
	if (dnslist): return dnslist
	
	dnsrequest.nameservers = [dnsprovider3]
	dnslist = rundnsquery(dnsrequest,host)
	if (dnslist): return dnslist

	#now ipv6 providers
	dnsrequest.nameservers = [dnsprovider1ipv6]
	dnslist = rundnsquery(dnsrequest,host)
	if (dnslist): return dnslist	

	dnsrequest.nameservers = [dnsprovider2ipv6]
	dnslist = rundnsquery(dnsrequest,host)
	if (dnslist): return dnslist

	dnsrequest.nameservers = [dnsprovider3ipv6]
	dnslist = rundnsquery(dnsrequest,host)

	
	if (dnslist): return dnslist

	else:
		dnslist = ( (2,1,0, '', (manualtextmagicipv4_1,443)), (2,1,0, '', (manualtextmagicipv4_2,443)), (23,1,0, '', (manualtextmagicipv6_1, 443, 0, 0)), (23,1,0, '', (manualtextmagicipv6_2, 443, 0, 0)) )
		print("Falling back to final list")
		return dnslist



### This overloads a function in the socket library, otherwise you couldn't use alternate DNS servers
def my_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
	addrlist = []
	
		
	from socket import _socket
	from socket import _intenum_converter
	from socket import AddressFamily
	from socket import SocketKind
    	
    	#This code replaces the default if textmagic is the destination
	if (host=='rest.textmagic.com'):
		#this replaces our own dns call instead of the system call
		dnslist=getdnsip(host)
		for res in dnslist:			
			af, socktype, proto, canonname, sa = res
			addrlist.append((_intenum_converter(af, AddressFamily),_intenum_converter(socktype, SocketKind),proto, canonname, sa))
			
	else:
		for res in _socket.getaddrinfo(host, port, family, type, proto, flags):
			af, socktype, proto, canonname, sa = res
			addrlist.append((_intenum_converter(af, AddressFamily),_intenum_converter(socktype, SocketKind),proto, canonname, sa))

	#print(_socket.getaddrinfo(host, port, family, type, proto, flags))
	return addrlist

###Clears all routes that were added
def cleardnsroutes():
	os.system('route delete ' + dnsprovider1)
	os.system('route delete ' + dnsprovider2)
	os.system('route delete ' + dnsprovider3)
	os.system('route delete ' + dnsprovider1ipv6 + '/128')
	os.system('route delete ' + dnsprovider2ipv6 + '/128')
	os.system('route delete ' + dnsprovider3ipv6 + '/128')	

###Temporarily adds routes to dns providers
def adddnsroutes():
	os.system('route add ' + dnsprovider1 + ' ' + backupgwip + ' metric 5')
	os.system('route add ' + dnsprovider2 + ' ' + backupgwip + ' metric 5')
	os.system('route add ' + dnsprovider3 + ' ' + backupgwip + ' metric 5')
	#This probably won't work - check your interface
	os.system('netsh interface ipv6 add route ' + dnsprovider1ipv6 + '/128 interface=\"' + ipv6intnum + '\" ' + backupgwipv6 )
	os.system('netsh interface ipv6 add route ' + dnsprovider2ipv6 + '/128 interface=\"' + ipv6intnum + '\" ' + backupgwipv6 )
	os.system('netsh interface ipv6 add route ' + dnsprovider3ipv6 + '/128 interface=\"' + ipv6intnum + '\" ' + backupgwipv6 )

###Checks for internet access by pinging a lot of different places
###It only requires one success
def checkinternet():
	up=False

	hostname = dnsprovider1
	response = os.system("ping -n 1 " + hostname)
	if response == 0:
		return True

	hostname = dnsprovider2
	response = os.system("ping -n 1 " + hostname)
	if response == 0:
		return True

	hostname = dnsprovider3
	response = os.system("ping -n 1 " + hostname)
	if response == 0:
		return True

	hostname = dnsprovider1ipv6
	response = os.system("ping -n 1 " + hostname)
	if response == 0:
		return True		

	hostname = dnsprovider2ipv6
	response = os.system("ping -n 1 " + hostname)
	if response == 0:
		return True

	hostname = dnsprovider3ipv6
	response = os.system("ping -n 1 " + hostname)
	if response == 0:
		return True		
	
	return up

### This attempts to send the text out of the alternate route	
def send_message_alt_route():
	
	#This lets us know if we were able to send the message
	messagesent=True
	
	#We need the backup route to the DNS servers since the primary failed
	adddnsroutes()
	
	#We now get the dns results for textmagic
	dnslist=getdnsip('rest.textmagic.com')
	
	#We add a route out to the backup gateway for each textmagic ip
	for rdata in dnslist:
		routetype = rdata[0]
		routeip = rdata[4][0]
		if (routetype==2):
			os.system('route add ' + routeip + ' ' + backupgwip + ' metric 5')
		else:
			os.system('netsh interface ipv6 add route ' + routeip + '/128 interface=\"' + ipv6intnum + '\" ' + backupgwipv6 )
			
		
	#We try to send the message		
	try:
		client.messages.create(lists=recipients, text=arguments)
				
	except BaseException as e:
		print(e)
		#We failed, so return a failed value
		messagesent = False
				
	for rdata in dnslist:
		routetype = rdata[0]
		routeip = rdata[4][0]
		if (routetype==2):
			os.system('route delete ' + routeip )
		else:
			os.system('route delete ' + routeip + '/128')
				
	cleardnsroutes()
	return messagesent

#Here we replace the socket function and initialize the textmagic client
from textmagic.rest import TextmagicRestClient
import textmagic.rest as tm
tm.models.base.httplib2.socket.getaddrinfo = my_getaddrinfo
client = tm.TextmagicRestClient(username, apikey)



#If the program failed, routes may remain
### Here we make sure we clear any forced routes
cleardnsroutes()

#Here we start testing for Internet access.  Only one success is needed
up=checkinternet()


# if we have internet access, simply send it
if (up):
	try:
		client.messages.create(lists=recipients, text=arguments)
	except BaseException as e:
		print(e)
		#Well, that didn't work.  Better try plan B
		up = False
	
#if not, we test the backup gateway
if (not up):

	#checks to see if we have internet out the backup connection
	adddnsroutes()
	up=checkinternet()
	cleardnsroutes()
	
	#clean up the ping test routes
	
	
	if (up):
		#Try to send our message
		#If we fail it will try again
		up=send_message_alt_route()
		
			
	
	if (not up):
		#If everything fails, just try to send it anyway, by any means		
		try:
			client.messages.create(lists=recipients, text=arguments)
			
		except BaseException as e:
			print(e)
		
		#Now try with the other routes
		send_message_alt_route()
		
				
	
	
	

