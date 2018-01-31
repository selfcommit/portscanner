# portscanner

Description
Determining the identity of a webserver is a hard problem. 
One consistant method is to ask the webserver. Unfortunately there's no promise the server will respond honestly.

ipscanner is written as a tool to provide a best guess about webservers based on header response.

ipscanner is written for python3, but may work with some versions of python2.

Input
- flag with ips
- file with ips comma separated?

Limitations
- Does not anticipate SSL?
- Servers outside of IIS or nginx?
- 


Notes:
# wget spider https://superuser.com/questions/642555/

# List directory contents with bs4 https://stackoverflow.com/questions/11023530