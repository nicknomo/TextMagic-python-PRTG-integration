#This was written in Python 3
# REQUIRES DNS PYTHON http://www.dnspython.org/
# REQUIRES textmagic python library https://www.textmagic.com/docs/api/python/
import sys
import os
import dns.resolver
from textmagic.rest import TextmagicRestClient

 
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
#Put the relevant list id into here

recipients='999999'


#This is the backup gateway ip if you have one

backupgwip = '192.168.1.2'

##### END OF USER CONFIGURABLE SECTION #####
##### END USER CONFIGURABLE SECTION #####



###### MAIN CODE #######
#### DO NOT EDIT #######
###### MAIN CODE #######

#Initialize the client object - provided by the textmagic library
client = TextmagicRestClient(username, apikey)

#we take the arguments, and remove the server name
#this makes it easier on the text2speech engine - it gets right to the point
#the PRTG output is then repeated and repeated
#this allows the user to keep listening, since the text2speech can be spotty
args = sys.argv[1:]
arguments = ''.join(str(x)+' ' for x in args)
breakpoint = arguments.find(']')
arguments = arguments[breakpoint+2:]
arguments = arguments+arguments+arguments+arguments+arguments+arguments+arguments+arguments+arguments




#Here we start testing for Internet access.  Only one success is needed
up=False

hostname = "8.8.8.8"
response = os.system("ping -n 1 " + hostname)
if response == 0:
	up = True

hostname = "8.8.4.4"
response = os.system("ping -n 1 " + hostname)
if response == 0:
	up = True

hostname = "139.130.4.5"
response = os.system("ping -n 1 " + hostname)
if response == 0:
	up = True


# if we have internet access, simply send it
if (up):
	try:
		client.messages.create(lists=recipients, text=arguments)
	except BaseException as e:
		print(e)
	
#if not, we test the backup gateway
else:

	os.system('route add 8.8.8.8 ' + backupgwip + ' metric 5')
	os.system('route add 8.8.4.4 ' + backupgwip + ' metric 5')
	os.system('route add 139.130.4.5 ' + backupgwip + ' metric 5')
	
	
	
	up=False
	
	hostname = "8.8.8.8"
	response = os.system("ping -n 1 " + hostname)
	if response == 0:
		up = True
	
	hostname = "8.8.4.4"
	response = os.system("ping -n 1 " + hostname)
	if response == 0:
		up = True
	
	hostname = "139.130.4.5"
	response = os.system("ping -n 1 " + hostname)
	if response == 0:
		up = True
	
	#clean up the ping test routes
	os.system('route delete 8.8.8.8 ')
	os.system('route delete 8.8.4.4 ')
	os.system('route delete 139.130.4.5 ')
	
	if (up):
		try:
			answers = dns.resolver.query('rest.textmagic.com', 'A')
			for rdata in answers:
				routeip = rdata.to_text()
				os.system('route add ' + routeip + ' ' + backupgwip + ' metric 5')
		
			try:
				client.messages.create(lists=recipients, text=arguments)
			
			except BaseException as e:
				print(e)
			
			for rdata in answers:
				routeip = rdata.to_text()
				os.system('route delete ' + routeip )
			
		
		except BaseException as e:
			print (e)	

	else:
		#If everything fails, just try to send it anyway, by any means		
		try:
			client.messages.create(lists=recipients, text=arguments)
			
		except BaseException as e:
			print(e)
		
		#Now try with the other routes
		try:
			answers = dns.resolver.query('rest.textmagic.com', 'A')	
			for rdata in answers:
				routeip = rdata.to_text()
				os.system('route add ' + routeip + ' ' + backupgwip + ' metric 5')
			
			try:
				client.messages.create(lists=recipients, text=arguments)
				
			except BaseException as e:
				print(e)
						
			#now delete the routes
			for rdata in answers:
				routeip = rdata.to_text()
				os.system('route delete ' + routeip )
		
		
		except BaseException as e:
			print (e)


