import os

import requests
import yaml
from lettuce import step, world
from requests import ConnectionError

from test_config import ANSIBLE_HOSTS_FILE, ANSIBLE_PLAYBOOK_FILE
from utils import run_cmd

MONGO_RESPONSE = 'It looks like you are trying to access MongoDB over HTTP on the native driver port.\n'


def parse_hosts(ansible_host_file):
	with open(ansible_host_file, "r") as f:
		result = yaml.load(f).get("all").get("hosts")
	return result


@step('file with Ansible configuration')
def get_command(step_instance):
	world.ansible_host_file = ANSIBLE_HOSTS_FILE


@step('checked if file exists')
def check_if_exists(step_instance):
	file_exists = os.path.isfile(world.ansible_host_file)
	assert file_exists, "File {} doesn't exist".format(world.ansible_host_file)
	world.ansible_hosts = parse_hosts(world.ansible_host_file)


@step("Ansible deployment passed")
def step_impl(step_instance):
	run_cmd('ansible-playbook -i {} -e "ansible_python_interpreter=/usr/bin/python3" {}'.format(
		ANSIBLE_HOSTS_FILE,
		ANSIBLE_PLAYBOOK_FILE
	))
	


@step("MongoDB is available at port (\d+)")
def step_impl(step_instance, port):
	for host in world.ansible_hosts.keys():
		try:
			r = requests.get("http://{}:{}/".format(host, port))
			status = r.content == MONGO_RESPONSE
		except ConnectionError:
			status = False
		assert status, "MongoDB is not available at https://{}:{} ".format(host, port)
