import os
import subprocess

import boto3
from botocore.exceptions import ClientError

from test_config import TERRAFORM_DIR, PACKER_DIR, PACKER_CONFIG_FILES


def run_cmd(cmd, env=None):
	"""
	runs a shell command
	
	:type env: dict
	:param env:
	:type cmd: str
	:param cmd: shell command
	:return: output of the command
	"""
	process = subprocess.Popen(
		cmd,
		shell=True,
		stdin=subprocess.PIPE,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
		close_fds=False,
		env=env,
	)
	out, err = process.communicate()
	return out, err


class TFRunner(object):
	"""
	Terraform s3_runner
	"""
	
	def __init__(self, config_dir=".", variables=None):
		"""
		Creates a terraform wrapper
		:type config_dir: str
		:param config_dir:
		:type variables: dict
		:param variables:
		"""
		self.config_dir = config_dir
		self.variables = variables if variables is not None else {}
	
	def __run_command(self, command):
		"""
		This function runs a terraform command with appropriate
		environmental variables and in a valid directory
		
		:type command: str
		:param command: command to be executed
		
		:return:
		"""
		env = os.environ
		if self.variables is not None:
			env.update({"TF_VAR_" + key: value for key, value in self.variables.items()})
		working_dir = os.getcwd()
		os.chdir(self.config_dir)
		
		out, err = run_cmd(command, env)
		
		os.chdir(working_dir)
		return out, err
	
	def init(self, backend_config=None):
		"""
		:type backend_config: dict
		:param backend_config: configuration of terraform backend
		:return:
		"""
		
		command_template = "terraform init{}"
		conf = ""
		if backend_config and type(backend_config) is dict:
			conf = " " + " ".join(
				map(
					lambda key: '-backend-config="{}={}"'.format(key, backend_config[key]),
					backend_config
				)
			)
		command = command_template.format(conf)
		return self.__run_command(command)
	
	def plan(self):
		"""
		
		:return:
		"""
		command_template = "terraform plan{}"
		command = command_template.format("")
		return self.__run_command(command)
	
	def apply(self):
		"""
		
		:return:
		"""
		command_template = "terraform apply{}"
		command = command_template.format(" -auto-approve")
		return self.__run_command(command)
	
	def destroy(self):
		"""
		
		:return:
		"""
		command_template = "terraform destroy{}"
		command = command_template.format(" -force")
		return self.__run_command(command)


class PackerRunner(object):
	def __init__(self, config_dir, config_file, variables=None):
		"""
		:type config_dir: str
		:param config_dir:
		:type config_file: str
		:param config_file:
		:type variables: dict
		:param variables:
		"""
		self.variables = variables
		self.config_dir = config_dir
		self.config_file = config_file
	
	def __run_command(self, command):
		"""
		This function runs a terraform command with appropriate
		environmental variables and in a valid directory

		:type command: str
		:param command: command to be executed

		:return:
		"""
		options = ""
		if self.variables is not None:
			options = " ".join(map(
				lambda key: "-var '{}={}'".format(key, self.variables[key]),
				self.variables
			))
		
		command += " " + options + " " + self.config_file
		
		working_dir = os.getcwd()
		os.chdir(self.config_dir)
		
		out, err = run_cmd(command)
		
		os.chdir(working_dir)
		return out, err
	
	def validate(self):
		command = "packer validate"
		return self.__run_command(command)
	
	def build(self, force=False):
		command = "packer build"
		if force:
			command += " -force"
		return self.__run_command(command)
	
	def delete(self):
		result = delete_image_if_exists(self.variables["ami_name"], self.variables["region"])
		error = None
		if not result:
			error = "Failed to delete the image"
		return result, error


def bucket_exists(bucket_name, cfg=None):
	"""
	Checks if the bucket with current name exists
	
	:type bucket_name: str
	:param bucket_name: the name of the bucket to check
	:type cfg: dict
	:param cfg: AWS configuration
	:rtype: bool
	:return: whether bucket exists or not
	"""
	if cfg is None:
		cfg = {
			"aws_region": "us-west-2"
		}
	result = True
	try:
		s3 = boto3.resource('s3', region_name=cfg['aws_region'])
		s3.meta.client.head_bucket(Bucket=bucket_name)
	except ClientError as e:
		# If a client error is thrown, then check that it was a 404 error.
		# If it was a 404 error, then the bucket does not exist.
		error_code = int(e.response['Error']['Code'])
		if error_code == 404:
			result = False
	return result


def vpc_exists(region, name):
	"""
	:type region: str
	:param region:
	:type name: str
	:param name:
	:return:
	"""
	ec2 = boto3.resource('ec2', region_name=region)
	vpc_filters = [{'Name': 'tag:Name', 'Values': [name]}]
	return len(list(ec2.vpcs.filter(Filters=vpc_filters))) > 0


def get_images(name, region):
	"""
	:type name: str
	:param name:
	:type region: str
	:param region:
	:rtype: list
	:return:
	"""
	ec2 = boto3.resource('ec2', region_name=region)
	image_filters = [{'Name': 'name', 'Values': [name + "-*"]}]
	images = ec2.images.filter(Filters=image_filters)
	return images


def image_exists(name, region):
	"""
	:type name: str
	:param name:
	:type region: str
	:param region:
	:return:
	"""
	images = list(get_images(name, region))
	return len(images) > 0


def delete_image_if_exists(name, region):
	"""
	:type name: str
	:param name:
	:type region: str
	:param region:
	:return:
	"""
	images = list(get_images(name, region))
	if len(images) > 0:
		images[-1].deregister()
		return True
	else:
		return False


def cluster_exists(region, cluster_name, domain, count=1):
	"""
	Checks if cluster with <count> nodes exists
	with instance pattern <cluster_name>-<node_number>.<domain>
	
	:param region: AWS region
	:type region: str
	:param cluster_name: name of the cluster
	:type cluster_name: str
	:param domain: domain used for a cluster
	:type domain: str
	:param count: number of nodes in cluster
	:type count: int
	:return: whether cluster exists or not
	:rtype: bool
	"""
	instance_pattern = cluster_name + "-*." + domain
	instances = get_instances(region, instance_pattern, cluster_name)
	success = len(instances) == count
	return success


def get_instances(region, instance_pattern="*", cluster_name="*"):
	"""
	Gets all instances from the cluster in a region with name matching the pattern

	:param region: the name of a region in which to search
	:type region: str
	:param instance_pattern: the pattern of instance name
	:type instance_pattern: str
	:param cluster_name: the name of cluster to get data from
	:type cluster_name: str
	:return: list with instance data
	:rtype: dict
	"""
	
	ec2 = boto3.client('ec2', region_name=region)
	instances = ec2.describe_instances(Filters=[
		{
			'Name': 'tag:Name',
			'Values': [instance_pattern]
		},
		{
			'Name': 'instance-state-name',
			'Values': ['running']
		},
		{
			'Name': 'tag:cluster',
			'Values': [cluster_name]
		},
	])
	instances = instances.get("Reservations")
	return instances


def get_security_groups(aws_region, customer, project_name):
	"""
	
	:param aws_region:
	:param customer:
	:param project_name:
	:return:
	"""
	ec2 = boto3.client('ec2', region_name=aws_region)
	sg_pattern = "{}-{}-security-group".format(customer, project_name)
	sg = ec2.describe_security_groups(Filters=[
		{
			'Name': 'tag:Name',
			'Values': [sg_pattern + "*"]
		},
	]).get("SecurityGroups")
	return sg


def sg_exists(aws_region, customer, project_name):
	return len(get_security_groups(aws_region, customer, project_name)) > 0


def security_group_has_port_allowed(sg, port):
	"""
	Gets information whether the port is enabled in current security group
	Format of sg should be the output of boto3.client('ec2').describe_security_groups
	:param sg: data of security group
	:type sg: dict
	:param port: allowed port in security grout
	:type port: int
	:return: port is enabled or not
	:rtype: bool
	"""
	port_is_open = False
	
	for permission in sg["IpPermissions"]:
		if permission.get('ToPort') == port and {u'CidrIp': '0.0.0.0/0'} in permission.get('IpRanges'):
			port_is_open = True
			break
	return port_is_open


def iam_role_exists(name):
	role_exists = False
	iam = boto3.client('iam')
	roles = iam.list_roles().get("Roles")
	for role in roles:
		if name in role.get("RoleName"):
			role_exists = True
			break
	return role_exists


def main():
	tf_s3_config = {
		"customer": "flugel-test",
		"terraform_bucket_name": "terraform-state",
		"aws_region": "us-west-2",
	}
	s3_runner = TFRunner(TERRAFORM_DIR["S3"], tf_s3_config)
	
	# print("Planning S3")
	# out, err = s3_runner.plan()
	#
	# print("Applying S3")
	# out, err = s3_runner.apply()
	
	tf_aws_config = {
		"customer": tf_s3_config["customer"],
		"aws_region": "eu-west-2",
		"project_name": "aws-vpc",
		"tf_region": tf_s3_config["aws_region"],
		"namespace": "cluster_test",
		"public_key_path": "~/.ssh/id_rsa.pub",
	}
	tf_aws_init_config = {
		"bucket": "{}-{}".format(tf_aws_config['customer'], tf_s3_config['terraform_bucket_name']),
		"key": "{}/terraform.tfstate".format(tf_aws_config["project_name"]),
		"region": tf_aws_config["tf_region"],
	}
	aws_runner = TFRunner(TERRAFORM_DIR["AWS"], tf_aws_config)
	
	# print("Initializing AWS")
	# aws_runner.init(tf_aws_init_config)
	
	# print("Planning AWS")
	# out, err = aws_runner.plan()
	#
	# print("Applying AWS")
	# out, err = aws_runner.apply()
	#
	# print(out)
	# print(err)
	#
	# vpc_exists = check_if_vpc_exists(tf_aws_config['aws_region'], tf_aws_config['namespace'])
	# if vpc_exists:
	# 	print("VPC {} exists".format(tf_aws_config['namespace']))
	# else:
	# 	print("VPC {} doesn't exist".format(tf_aws_config['namespace']))
	
	# vpc_exists = check_if_vpc_exists(tf_aws_config['aws_region'], tf_aws_config['namespace'])
	# if vpc_exists:
	# 	print("VPC {} exists".format(tf_aws_config['namespace']))
	# else:
	# 	print("VPC {} doesn't exist".format(tf_aws_config['namespace']))
	
	packer_ubuntu_config = {
		"region": tf_aws_config["aws_region"],
		"ami_name": "mongodb-ubuntu-test"
	}
	packer_ubuntu_runner = PackerRunner(PACKER_DIR, PACKER_CONFIG_FILES["ubuntu"], packer_ubuntu_config)
	
	# print("Validating Ubuntu image")
	# out, err = packer_ubuntu_runner.validate()
	#
	# print("Building Ubuntu image")
	# out, err = packer_ubuntu_runner.build(force=True)
	#
	# print("Deleting Ubuntu image")
	# out, err = packer_ubuntu_runner.delete()
	
	packer_centos_config = {
		"region": tf_aws_config["aws_region"],
		"ami_name": "mongodb-centos-test"
	}
	packer_centos_runner = PackerRunner(PACKER_DIR, PACKER_CONFIG_FILES["centos"], packer_centos_config)
	
	# print("Validating Centos image")
	# out, err = packer_centos_runner.validate()
	#
	# print("Building Centos image")
	# out, err = packer_centos_runner.build(force=True)
	#
	# print("Deleting Centos image")
	# out, err = packer_centos_runner.delete()
	#
	# print(out)
	# print(err)
	
	tf_mongodb_config = {
		"customer": tf_s3_config["customer"],
		"aws_region": tf_aws_config["aws_region"],
		"tf_region": tf_s3_config["aws_region"],
		"namespace": tf_aws_config["namespace"],
		"project_name": "mongodb-cluster",
		"os_env": "ubuntu",
		"instance_count": "3",
		"cluster_name": "cluster_test",
		"dns_domain": "flugel-it.com",
		"key_name": tf_aws_config["namespace"]
	}
	tf_mongodb_init_config = {
		"bucket": "{}-{}".format(tf_mongodb_config['customer'], tf_s3_config['terraform_bucket_name']),
		"key": "{}/terraform.tfstate".format(tf_mongodb_config["project_name"]),
		"region": tf_mongodb_config["tf_region"],
	}
	
	mongodb_runner = TFRunner(TERRAFORM_DIR["MongoDB"], tf_mongodb_config)
	
	# print("Initializing MongoDB")
	# out, err = mongodb_runner.init(tf_mongodb_init_config)
	# print("Planning MongoDB")
	# out, err = mongodb_runner.plan()
	# print("Applying MongoDB")
	# out, err = mongodb_runner.apply()
	# print("Destroying MongoDB")
	# out, err = mongodb_runner.destroy()
	
	# print(out)
	# print(err)
	
	# print("Destroying AWS")
	# out, err = aws_runner.destroy()
	#
	# print(out)
	# print(err)
	
	# print("Destroying S3")
	# out, err = s3_runner.destroy()
	#
	# print(out)
	# print(err)
	
	# created_successfully = cluster_exists(
	# 	tf_mongodb_config["aws_region"],
	# 	tf_mongodb_config["cluster_name"],
	# 	tf_mongodb_config["dns_domain"],
	# 	int(tf_mongodb_config["instance_count"]),
	# )
	#
	# print(created_successfully)
	
	# sg = get_security_groups(
	# 	tf_mongodb_config["aws_region"],
	# 	tf_mongodb_config["customer"],
	# 	tf_mongodb_config["project_name"]
	# )
	#
	# port = 23
	# if len(sg) > 0:
	# 	sec_group = sg[0]
	# 	port_is_open = security_group_has_port_allowed(sec_group, port)
	# 	print(port_is_open)
	
	# role_exists = iam_role_exists(tf_mongodb_config["namespace"] + "-cluster-join_")
	# print(role_exists)
	
	print("Finished")


if __name__ == '__main__':
	main()
