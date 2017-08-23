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
#On the textmagic Web UI contacts section to make contacts and then a list. Set the contacts to "landline"
#The easiest way to get the list ID is to go to the lists page ( https://my.textmagic.com/online/messages/lists ), 
#and click on the appropriate list. The URL will end with the List ID. 
#For example: https://my.textmagic.com/online/contacts/list/999999 , where the list ID would be 999999 .

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
	
