ANSIBLE_HOSTS_FILE = "../hosts.yml"
ANSIBLE_PLAYBOOK_FILE = "../mongodb/ansible/mongodb-ubuntu/playbook.yml"

S3_TERRAFORM_DIR = "../s3/terraform/"

try:
	from test_config_local import *
finally:
	pass
