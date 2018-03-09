import os
import subprocess

import boto3
from botocore.exceptions import ClientError


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
	Terraform runner
	"""
	
	def __init__(self, config_dir=".", variables=None):
		"""
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
	
	def init(self):
		"""
		
		:return:
		"""
		command_template = "terraform init{}"
		command = command_template.format("")
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


def check_if_bucket_exists(bucket_name, cfg=None):
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

# if __name__ == '__main__':
# 	tf_s3_config = {
# 		"customer": "flugel-test",
# 		"terraform_bucket_name": "terraform-state",
# 		"aws_region": "us-west-2",
# 	}
# 	runner = TFRunner("../s3/terraform/", tf_s3_config)
# 	print "Planning"
# 	runner.plan()
#
# 	print "Applying"
# 	runner.apply()
#
# 	print "Destroying"
# 	runner.destroy()
#
# 	bucket_name = "{}-{}".format(tf_s3_config['customer'], tf_s3_config['terraform_bucket_name'])
# 	config = {
# 		"aws_region": tf_s3_config["aws_region"]
# 	}
# 	print check_if_bucket_exists(bucket_name, config)
