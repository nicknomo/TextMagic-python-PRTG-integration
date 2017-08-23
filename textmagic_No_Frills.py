#This was written in Python 3
# REQUIRES DNS PYTHON http://www.dnspython.org/
# REQUIRES textmagic python library https://www.textmagic.com/docs/api/python/
import sys
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


##### END OF USER CONFIGURABLE SECTION #####
##### END USER CONFIGURABLE SECTION #####



###### MAIN CODE #######
#### DO NOT EDIT #######
###### MAIN CODE #######

#Initialize the client object - provided by the textmagic library
client = TextmagicRestClient(username, apikey)


#the PRTG output is then repeated twice
#this allows the user to keep listening, since the text2speech can be spotty
args = sys.argv[1:]
arguments = ''.join(str(x)+' ' for x in args)
arguments = arguments+arguments



try:
  client.messages.create(lists=recipients, text=arguments)
except BaseException as e:
  print(e)
	
