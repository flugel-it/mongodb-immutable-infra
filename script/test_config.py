ANSIBLE_HOSTS_FILE = "../hosts.yml"
ANSIBLE_PLAYBOOK_FILE = "../mongodb/ansible/mongodb-ubuntu/playbook.yml"

TERRAFORM_DIR = {
	"S3": "../s3/terraform/",
	"AWS": "../aws/terraform/",
	"MongoDB": "../mongodb/terraform/"
}

PACKER_DIR = "../mongodb/packer/"
PACKER_CONFIG_FILES = {
	"ubuntu": "mongodb-ubuntu.json",
	"centos": "mongodb-centos.json",
}

RUNNER_TEMPLATE = {
	"S3": None,
	"AWS": None,
	"MongoDB": None,
}

CONFIG_TEMPLATE = {
	"S3": {},
	"AWS": {},
	"MongoDB": {},
}

# override existing variables in test_config_local if needed
try:
	from test_config_local import *
except ImportError:
	pass
