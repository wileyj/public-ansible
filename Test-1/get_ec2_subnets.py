#!/usr/bin/python
import subprocess, json
cmd = subprocess.Popen('ec2-describe-subnets', shell=True, stdout=subprocess.PIPE)
data = [{}]
for line in cmd.stdout:
  line = line.strip()
  if "TAG" in line:
    parts = line.split("\t")
    json_string = {parts[4] : parts[2]}
    data[0][parts[4]] = parts[2]
json_encode = json.dumps(data)        
print json_encode


