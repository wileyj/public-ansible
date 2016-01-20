#!/usr/bin/python
# 192.168.56.105 is the asset tracker test project
import urllib2, json, sys, socket, time, requests
from math import trunc
hostname = socket.gethostname()
ip = socket.gethostbyname(socket.gethostname())
time = time.time()
time = trunc(time)
os_name=''
os_version=''
inputfile = open('/etc/redhat-release')
for line in inputfile:
	#print 'line:',line
	value = line.split(" ")
	os_name = value[0]
	os_version = value[2]

print 'hostname:',hostname
print 'ip:', ip
print 'time:',time
print 'os_name:', os_name
print 'os_version:', os_version
data = {
        'type'            : "host",
        'hostname'        : hostname,
        'ip'              : ip,
        'mtime'           : time,
        'os_id'           : os_name,
        'os_name'         : os_name,
        'os_version_name' : os_version,
        'os_version_id'   : os_version
}
url = 'http://192.168.56.105/REST/v1/update'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post(url, data=json.dumps(data), headers=headers)
#print 'response:',r
sys.exit(r.text)
