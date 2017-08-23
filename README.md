# TextMagic-python-PRTG-integration
PRTG runs this Windows script in order to send a notification

This is made with the purpose of 
1) using a primary and backup gateway to ensure your textmagic message gets out
2) Using the text to speech feature (getting phone calls instead of texts)
3) Using PRTG with windows

This is a very niche oriented usage, and this code is probably not useful to most people. Nevertheless, PRTG users relying on alerts may not receive emails or texts if a gateway goes down, or a DNS server goes down.  The textmagic.py file will handle a single gateway failure. The textmagic_SUPER_HA.py is more robust and will handle a single gateway failure, but also takes into account the possibility of total dns failure.   

#### REQUIRES PYTHON 3. This was written in PYTHON 3, and will not work with Python2 . I recommend WinPython if you are using windows. https://sourceforge.net/projects/winpython/files/WinPython_3.4/3.4.4.6/

#### REQUIRES DNS PYTHON http://www.dnspython.org/ - can be installed by "pip install dnspython"

#### REQUIRES textmagic python library https://www.textmagic.com/docs/api/python/ - The "pip install textmagic" did not work properly for me. You may need to download the zip, and place the textmagic folder in the same directory as the textmagic.py file.

#### REQUIRES httplib2 library https://pypi.python.org/pypi/httplib2  - textmagic depends on this, and will be installed if you run "pip install textmagic". Otherwise, you can install it by itself by typing "pip install httplib2" .


I've included the sources for the textmagic and dns python.  You should try and download these libraries from their respective sources, and you should not need these. Using "pip install" from the Winpython command line is highly recommended. I've included them in this repo in case their functionality or structure changes at a later date. 

## SUPER HA VERSION

The super ha version is more complicated, but it uses its own dns lookups to try and complete the task.  In the case of local DNS outages, this would still work.  It attempts ipv4 and ipv6. If you choose this version, simply rename it textmagic.py (so the .bat file will execute it), or change the batch file to call it by its current name. 



# Configuration

## 1) Download the Proper files

#### Please download both textmagiclauncher.bat and textmagic.py (if you choose to use textmagic_SUPER_HA.py, please rename it textmagic.py). Place the textmagic.bat file in C:\Program files (x86)\PRTG Network Monitor\Notifications\EXE\ (for the 32 bit version, its C:\Program files\PRTG Network Monitor\Notifications\EXE\ ) . The textmagic.py file can go anywhere, but for security purposes it should not go where non-Administrator Users have write access.

## 2) Edit textmagiclauncher.bat

#### The textmagiclauncher.bat file will need to be changed so that the correct python.exe and textmagic.py locations are specified. The default is:

```
"C:\Program Files\Python\python-3.4.4.amd64\python.exe" "C:\Program Files\Python\python-3.4.4.amd64\textmagic.py" %*
```

#### but your python folder may be different, as well as where you've stored textmagic.py. For example, the configuration might be changed to:

```
"C:\python\python.exe" "C:\users\administrator\python\textmagic.py" %*
```

#### Note; do not remove the %* at the end.  That allows the PRTG passed information to be sent to the textmag.py python program. Without this, your textmagic call will not contain any information and may not even be sent.  

## 3) Install Python dependencies

#### It is recommended that you run the following commands:

```
pip install dnspython
pip install httplib2
pip install textmagic
```

#### The pip install of textmagic did not work for me, so I downloaded the textmagic repo from github and put the textmagic folder in the same place as my textmagic.py file.  

## 4) Edit the textmagic.py file

#### Several parts of the textmagi.py will need to be changed:

#### The following need to be changed to reflect what is found on the textmagic API page.

```
username = "usernamegoeshere"
apikey = "Rasd123sdfsdfscszxxzorsomething"
```

#### For Text2speech, the recipient has to be a member of list. On the textmagic Web UI contacts section to make a list and the contacts, set them manually to landline. Go to the Web ui's services secion, go to text to speech, and set it to enabled for landline phones.

#### Now go to the sandbox section and user GET /api/v2/lists/search . The URL is https://rest.textmagic.com/api/v2/doc#get--api-v2-lists-search . Hit sandbox, and then hit the TRY button. Your lists ids will be in there. NOTE: the username and api token need to be entered at the very top of the sandbox page.

#### Enter the relevant list id into here
```
recipients='999999'
```

## 5) Enter a backup gateway for ipv4 and ipv6

#### If you don't havea backup gateway, most of the features of this program aren't going to be very helpful. You can simply put the primary gateway again.  If you don't use ipv6, you don't have to worry too much about it.  The ipv6 related commands will fail, but this doesn't matter.

#### If you have an ipv4 backup gateway, enter it here:
```
backupgwip = '192.168.1.2'
```
#### Your ipv6 backup gateway can be entered here, however the corret interface number needs to be entered as well.  To get the interface number, enter this command from the command line:  netsh int ipv4 show interfaces  . Enter the numeric value into the ipv6intnum variable.  The default is interface 1, and is likely not to be correct. This is only available in the SUPER_HA version.
```
backupgwipv6 = 'fd00:0:0:1::2'
ipv6intnum = '1'
```

## 6) (OPTIONAL) Choose backup DNS Servers (Internet based only!) - only available in the SUPER_HA version

#### On the first attempt, your system's default nameservers are used. These variables are for BACKUP DNS ATTEMPTS, and INTERNET CONNECTIVITY CHECKS. Please do not put your system's default DNS servers in here. Its best to use public and highly available dns servers. DO NOT USE INTERNAL SERVERS! THIS WILL DEGRADETHE USEFULNESS OF THIS PROGRAM! These defaults are very good choices, but if you use any of these as your system's primary or secondary DNS server, you may want to change them.
```
dnsprovider1 = '8.8.8.8'
dnsprovider2 = '8.8.4.4'
dnsprovider3 = '4.2.2.1'
dnsprovider1ipv6 = '2001:4860:4860::8888'
dnsprovider2ipv6 = '2001:4860:4860::8844'
dnsprovider3ipv6 = '2001:470:1f10:c6::2'
```
## 7) (OPTIONAL) Manually add the current IP addresses of rest.textmagic.com 

#### In the event of a total DNS failure (e.g. firewall configuration error, QoS misconfiguration, etc), you will still want notifications to work. These entires will certainly become stale with time, but the textmagic IP's have been stable for around 6 months at a time. This is a method of last resort, and is unlikely to ever be used. To find the proper values, just do a dns lookup of rest.textmagic.com
```
manualtextmagicipv4_1 = '104.20.24.237'
manualtextmagicipv4_2 = '104.20.23.237'
manualtextmagicipv6_1 = '2400:cb00:2048:1::6814:18ed'
manualtextmagicipv6_2 = '2400:cb00:2048:1::6814:17ed'
```

## 8) Set EXE notification in PRTG

#### Go to Setup -> Account Settings -> Notifications. The default notification is "Email and push notification to admin".  You can edit it, and enable EXE notification. The textmagiclauncher.bat should be visible if you've put it in the right location. I suggest changing the following default settings:
```
Arguments:  %device %name %status %down,,,
Timeout:    180
```

#### See here for more information: https://www.paessler.com/manuals/prtg/notifications_settings  

# Debugging
Its recommended that you test this by manually running the batch file from a command line.  If you are missing a necessary library, or python dependency, this will be the easiest way to determine that.  I recommend you leave the API key blank (in the textmagic.py configuration)  during testing.  You will likely get an HTTP 401 error after executing, and your account balance will not be charged from testing.  

I recommend you test and simulate interface and DNS server failures.  You will likely see failure messages during failover testing, especially regarding ipv6 if you don't have an ipv6 capable connection.  As long as you eventually see HTTP 401 errors (assuming you've removed your API key to test), the program is working as expected.  Once the API key and username are entered correctly, this program should work properly.

Once You are ready to testin PRTG, put the API key into textmagic.py . You can then test the notification from PRTG in Setup->Account Settings->Notifications.  Hit the test button, and you should receive your call/text .
