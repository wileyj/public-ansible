#!/usr/bin/python
import subprocess, json

def get_regions(command):
  print 'get_regions(',command,')'
  cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
  parse_results(cmd.stdout, "regions")

def get_subnet(command):
  print 'get_subnet(',command,')'
  cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
  parse_results(cmd.stdout, "subnet")

def get_vpc(command):
  print 'get_vpc(',command,')'
  cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
  parse_results(cmd.stdout, "vpc")

def get_sec_group(command):
  print 'get_sec_group(',command,')'
  cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
  parse_results(cmd.stdout, "sec")


def parse_results(output, type):
  data = {}
  for line in output:
    line = line.strip()
    if "TAG" in line:
      parts = line.split("\t")
      if parts[3] == 'Name':
        json_string = {parts[4] : parts[2]}
        data[parts[4]] = parts[2]
    if "REGION" in line:
      parts = line.split("\t")
      json_string = {parts[1] : parts[1]}
      data[parts[1]] = parts[1]
  print_data(data, type)

def print_data(data, type):
  json_encode = json.dumps(data)
  if type == "subnet":
    f = open('json/subnet.json', 'w')
  if type == "vpc":
    f = open('json/vpc.json', 'w')
  if type == "sec":
    f = open('json/secgroup.json', 'w')
  if type == "regions":
    f = open('json/regions.json', 'w')

  f.write(json_encode)
  
get_subnet("ec2-describe-subnets")
get_vpc("ec2-describe-vpcs")
get_sec_group("ec2-describe-group")
get_regions("ec2-describe-regions")

