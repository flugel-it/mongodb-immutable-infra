from lettuce import step, world

from test_config import TERRAFORM_DIR, RUNNER_TEMPLATE
from utils import TFRunner

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
