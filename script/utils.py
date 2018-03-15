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
	:return:
	"""
	ec2 = boto3.resource('ec2', region_name=region)
	image_filters = [{'Name': 'name', 'Values': [name + "-*"]}]
	images = ec2.images.filter(Filters=image_filters)
	return list(images)


def image_exists(name, region):
	"""
	:type name: str
	:param name:
	:type region: str
	:param region:
	:return:
	"""
	images = get_images(name, region)
	return len(images) > 0


def delete_image_if_exists(name, region):
	"""
	:type name: str
	:param name:
	:type region: str
	:param region:
	:return:
	"""
	images = get_images(name, region)
	if len(images) > 0:
		images[-1].deregister()
		return True
	else:
		return False


if __name__ == '__main__':
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
		"aws_region": "eu-west-1",
		"project_name": "aws-vpc",
		"tf_region": tf_s3_config["aws_region"],
		"namespace": "cluster_automation_test",
		"public_key_path": "~/.ssh/id_rsa.pub"
	}
	tf_aws_init_config = {
		"bucket": "{}-{}".format(tf_aws_config['customer'], tf_s3_config['terraform_bucket_name']),
		"key": "{}/terraform.tfstate".format(tf_aws_config["project_name"]),
		"region": tf_aws_config["tf_region"],
	}
	aws_runner = TFRunner(TERRAFORM_DIR["AWS"], tf_aws_config)
	
	# print("Initializing AWS")
	# aws_runner.init(tf_aws_init_config)
	#
	# print("Planning AWS")
	# out, err = aws_runner.plan()
	#
	# print("Applying AWS")
	# out, err = aws_runner.apply()
	
	# print(out)
	# print(err)
	
	# vpc_exists = check_if_vpc_exists(tf_aws_config['aws_region'], tf_aws_config['namespace'])
	# if vpc_exists:
	# 	print("VPC {} exists".format(tf_aws_config['namespace']))
	# else:
	# 	print("VPC {} doesn't exist".format(tf_aws_config['namespace']))
	
	# print("Destroying AWS")
	# out, err = aws_runner.destroy()
	
	# vpc_exists = check_if_vpc_exists(tf_aws_config['aws_region'], tf_aws_config['namespace'])
	# if vpc_exists:
	# 	print("VPC {} exists".format(tf_aws_config['namespace']))
	# else:
	# 	print("VPC {} doesn't exist".format(tf_aws_config['namespace']))
	
	# print("Destroying S3")
	# s3_runner.destroy()
	
	packer_ubuntu_config = {
		"region": tf_aws_config["aws_region"],
		"ami_name": "mongodb-ubuntu-test"
	}
	packer_ubuntu_runner = PackerRunner(PACKER_DIR, PACKER_CONFIG_FILES["ubuntu"], packer_ubuntu_config)
	
	# print("Validating Ubuntu image")
	# out, err = packer_ubuntu_runner.validate()
	
	print("Building Ubuntu image")
	out, err = packer_ubuntu_runner.build(force=True)
	
	print("Deleting Ubuntu image")
	out, err = packer_ubuntu_runner.delete()
	print(out)
	print(err)
	
	print("Finished")
