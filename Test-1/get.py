#!/usr/bin/python
# 192.168.56.105 is the asset tracker test project

import subprocess,urllib, json, sys, getopt, datetime, jinja2, difflib

def main(argv):
    debug=0;
    try:
        opts, args = getopt.getopt(argv,"dhH:",["host="])
    except getopt.GetoptError:
        show_help(2);
    if len(opts) > 0:
        for opt, arg in opts:
            if opt == '-h':
                show_help(1)
            elif opt in ("-H", "--host"):
            	host = arg
	    elif opt in ("-d", "--debug"):
		debug = 1;
    else:
        show_help(-1)
    get_json(host, debug)
def show_help(exit):
    print 'get.py -H <host>'
    print 'exiting with status code:', exit
    sys.exit(exit)

def get_json(host, debug):
    print 'Retrieving Host:', host
    url = "http://192.168.56.105/REST/v1/get/"+host
    jsonurl = urllib.urlopen(url)
    text = json.loads(jsonurl.read())
    ctime = text["ctime"]
    mtime = text["mtime"]
    ip =  text["ip"]
    subnet_name = text["subnet_name"]
    environment_name = text["env_name"]
    os_name = text["os_name"]
    os_version_name = text["os_version_name"]
    aws_instance_name = text["aws_instance_name"]
    aws_region_name = text["aws_region_name"]
    subnet_id = text["subnet_id"]
    environment_id = text["env_id"]
    os_id = text["os_id"]
    os_version_id = text["os_version_id"]
    aws_instance_id = text["aws_instance_id"]
    aws_region_id = text["aws_region_id"]
    description = text["desc"]
    instance = text["instance"]
    aws_host_id = text["aws_host_id"]
    notes = text["notes"]
    hostname = text["hostname"]
    print 'debug: ', debug
    to_match = 'DB'
    seq=difflib.SequenceMatcher(None, subnet_name,to_match)
    is_DB = seq.ratio()*100
    if is_DB <= 40.0:
	ami_id = 'ami-123456'
    else:
        ami_id = 'ami-123457'

    if debug == 1:
    	print 'Retrieved Hostname:         ', hostname
    	print 'Retrieved Ctime:            ', ctime
    	print 'Retrieved Mtime:            ', mtime
    	print 'Retrieved IP:               ', ip
    	print 'Retrieved Subnet Name:      ', subnet_name
    	print 'Retrieved Environment Name: ', environment_name
    	print 'Retrieved OS Name:          ', os_name
    	print 'Retrieved OS version Name:  ', os_version_name
    	print 'Retrieved Aws Instance Name:', aws_instance_name
    	print 'Retrieved Aws Region Name:  ', aws_region_name
    	print 'Retrieved Subnet ID:        ', subnet_id
    	print 'Retrieved Environment ID:   ', environment_id
    	print 'Retrieved OS ID:            ', os_id
    	print 'Retrieved OS version ID:    ', os_version_id
    	print 'Retrieved Aws Instance ID:  ', aws_instance_id
    	print 'Retrieved Aws Region ID:    ', aws_region_id
    	print 'Retrieved Description:      ', description
    	print 'Retrieved Instance:         ', instance
        print 'Retrieved Host ID:          ', aws_host_id
        print 'Ratio DB Match:             ', is_DB
        print 'Using AMI:                  ', ami_id
    	print 'Retrieved Notes:            ', notes 
	
        command = ' ec2-describe-instance-status %s -F instance-state-code=16 >/dev/null 2>&1' %(aws_host_id)
	    print 'Checking if host %s is running...' %(hostname)
        cmd = subprocess.Popen(command, shell=True)
    	exitcode = cmd.wait();
        print 'cmd return code: ', exitcode

    if exitcode != 0:
    	templateLoader = jinja2.FileSystemLoader( searchpath="." )
    	templateEnv = jinja2.Environment( loader=templateLoader )
    	TEMPLATE_FILE = "templates/group_vars.j2"
    	template = templateEnv.get_template( TEMPLATE_FILE )
    	templateVars = { 
            "aws_environment"    : environment_id, 
    	    "aws_instance_type"  : aws_instance_id, 
    	    "aws_security_group" : subnet_id, 
    	    "aws_region"         : aws_region_id,
            "aws_ami"            : ami_id,
    	    "aws_hostname"       : hostname,
            "vpc_subnet"         : subnet_id,
            "vpc_name"           : environment_id
	    }
        outputText = template.render( templateVars )
        f = open('ansible_playbook/group_vars/all', 'w')
        f.write(outputText)
        print "Host: ", hostname, " ready for building"
    else:
        print "Error: Can't build\nHost %s is already running" %(hostname)


def datetimefilter(value, format='%Y/%m/%d %H:%M'):
    """convert a datetime to a different format."""
    return value.strftime(format)

if __name__ == "__main__":
    host=''
    debug=''
    main(sys.argv[1:])


