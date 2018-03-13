from lettuce import step, world

from test_config import TERRAFORM_DIR, RUNNER_TEMPLATE
from utils import TFRunner, check_if_bucket_exists

world.tf_runners = RUNNER_TEMPLATE.copy()


@step("terraform config for (S3|AWS|MongoDb) is (initialized|planned|applied|destroyed)")
def run_terraform_stage(step_instance, namespace, stage):
	if world.tf_runners.get(namespace) is None:
		world.tf_runners[namespace] = TFRunner(TERRAFORM_DIR.get(namespace), world.tf_configs)
	runner = world.tf_runners.get(namespace)
	
	if stage == "initialized":
		_, err = runner.init(world.tf_init_configs)
	elif stage == "planned":
		_, err = runner.plan()
	elif stage == "applied":
		_, err = runner.apply()
	elif stage == "destroyed":
		_, err = runner.destroy()
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
