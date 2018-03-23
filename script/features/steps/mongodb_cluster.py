from time import sleep

from lettuce import step, world

from test_config import CLUSTER_CREATION_TIMEOUT
from utils import cluster_exists, get_security_groups, security_group_has_port_allowed, iam_role_exists


@step(u'(\d+) instances are (created|deleted) successfully')
def then_every_instance_is_created_successfully(step, instance_count, stage):
	status = cluster_exists(
		world.tf_configs["aws_region"],
		world.tf_configs["cluster_name"],
		world.tf_configs["dns_domain"],
		int(world.tf_configs["instance_count"]),
	)
	if stage == "created":
		assert status, 'Instances in cluster {} were not created successfully'.format(world.tf_configs["cluster_name"])
	else:
		assert not status, 'Instances in cluster {} were not deleted successfully'.format(
			world.tf_configs["cluster_name"])


# @step(u'port (\d+) is open on all instances')
# def port_is_open(step, port):
# 	assert True, 'This step must be implemented'
#

@step("security group for the cluster is created and ports (\d+(?:,\d+)*) are opened")
def sg_exists_and_has_ports_open(step_instance, ports):
	groups = get_security_groups(
		world.tf_configs["aws_region"],
		world.tf_configs["customer"],
		world.tf_configs["project_name"]
	)
	ports = map(lambda p: int(p), ports.split(","))
	assert len(groups) > 0, "Security group wasn't created"
	for group in groups:
		for port in ports:
			assert security_group_has_port_allowed(group, port), "Security group has port {} disallowed".format(port)


@step("security group for the cluster is deleted")
def sg_exists_and_has_ports_open(step_instance):
	groups = get_security_groups(
		world.tf_configs["aws_region"],
		world.tf_configs["customer"],
		world.tf_configs["project_name"]
	)
	assert len(groups) == 0, "Security group wasn't deleted"


@step("IAM role with prefix ([A-Za-z0-9\-_]+) is (created|deleted)")
def iam_role_status(step_instance, role_prefix, stage):
	# role_prefix = world.tf_configs["namespace"] + "-cluster-join_"
	role_exists = iam_role_exists(role_prefix)
	if stage == "created":
		assert role_exists, "IAM role with prefix {} doesn't exist".format(role_prefix)
	else:
		assert not role_exists, "IAM role with prefix {} exists".format(role_prefix)


@step("waited until cluster is up")
def step_impl(step_instance):
	sleep(CLUSTER_CREATION_TIMEOUT)
