#!/bin/sh
yum install -y curl wget
curl -L http://opscode.com/chef/install.sh | bash
chef-solo -v
