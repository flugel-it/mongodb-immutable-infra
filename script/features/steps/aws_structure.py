from lettuce import step, world

from utils import check_if_vpc_exists


@step("VPC with name ([A-Za-z0-9\-_]*) is (doesn't exist|exists)")
def step_impl(step_instance, name, exists):
	bucket_status = check_if_vpc_exists(world.tf_configs['aws_region'], name)
	if exists == "exists":
		assert bucket_status, "VPC with name {} is doesn't exist"
	else:
		assert not bucket_status, "VPC with name {} is exists"
