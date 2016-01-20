#!/bin/sh
export ANSIBLE_HOST_KEY_CHECKING=False
ansible-playbook -vvvv ansible_playbook/site.yml -i ansible_playbook/hosts
