from lettuce import step, world

from test_config import S3_TERRAFORM_DIR
from utils import TFRunner, check_if_bucket_exists

world.s3_tf_runner = None
world.s3_tf_config = {}


@step("customer name ([A-Za-z0-9\-_]*)")
def get_customer_name(step_instance, customer):
	world.s3_tf_config['customer'] = customer


@step("terraform bucket name ([A-Za-z0-9\-_]*)")
def get_terraform_name(step_instance, bucket):
	world.s3_tf_config['terraform_bucket_name'] = bucket


@step("AWS region ([a-z]{2}-[a-z]+-[1-9])")
def get_aws_region(step_instance, aws_region):
	world.s3_tf_config['aws_region'] = aws_region


@step("terraform config is (initialized|planned|applied|destroyed)")
def run_terraform_stage(step_instance, stage):
	if world.s3_tf_runner is None:
		world.s3_tf_runner = TFRunner(S3_TERRAFORM_DIR, world.s3_tf_config)
	
	if stage == "initialized":
		_, err = world.s3_tf_runner.init()
	elif stage == "planned":
		_, err = world.s3_tf_runner.plan()
	elif stage == "applied":
		_, err = world.s3_tf_runner.apply()
	elif stage == "destroyed":
		_, err = world.s3_tf_runner.destroy()
	else:
		assert False, "Such operation doesn't exist"
	
	assert err == "", "Terraform config exited with error: {}".format(err)


@step("S3 bucket called ([A-Za-z0-9\-_]*) is (created|deleted)")
def check_bucket_state(step_instance, full_bucket_name, state):
	exists = check_if_bucket_exists(full_bucket_name)
	if state == "created":
		assert exists, "The bucket called {} is not created".format(full_bucket_name)
	elif state == "deleted":
		assert not exists, "The bucket called {} is not deleted".format(full_bucket_name)
	else:
		assert False, "Such state doesn't exist"
