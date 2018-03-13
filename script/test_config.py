ANSIBLE_HOSTS_FILE = "../hosts.yml"
ANSIBLE_PLAYBOOK_FILE = "../mongodb/ansible/mongodb-ubuntu/playbook.yml"

TERRAFORM_DIR = {
	"S3": "../s3/terraform/",
	"AWS": "../aws/terraform/",
	"MongoDB": "../mongodb/terraform/"
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

try:
	from test_config_local import *
except ImportError:
	pass
