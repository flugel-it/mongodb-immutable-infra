from time import sleep

from lettuce import step, world

from test_config import PACKER_DIR, PACKER_CONFIG_FILES, IMAGE_DELETE_TIMEOUT
from utils import image_exists, PackerRunner


@step("packer region is ([a-z]{2}-[a-z]+-[1-9])")
def assign_packer_region(step_instance, region):
	world.region = region


@step("packer AMI name is ([A-Za-z0-9\-_]*)")
def assign_packer_ami_name(step_instance, ami_name):
	world.ami_name = ami_name


@step("(validated|built|deleted) (\w+) image")
def run_packer_stage(step_instance, stage, distribution):
	packer_config = {
		"region": world.region,
		"ami_name": world.ami_name
	}
	packer_runner = PackerRunner(PACKER_DIR, PACKER_CONFIG_FILES[distribution], packer_config)
	if stage == "validated":
		_, err = packer_runner.validate()
	elif stage == "built":
		_, err = packer_runner.build()
	elif stage == "deleted":
		_, err = packer_runner.delete()
	else:
		err = "This stage doesn't exist"
	assert not err, "Packer config for {} exited with this error:\n".format(distribution) + err


@step("image was (created|deleted) successfully")
def check_image(step_instance, stage):
	if stage == "created":
		exists = image_exists(world.ami_name, world.region)
	else:
		exists = not image_exists(world.ami_name, world.region)
	
	assert exists, "Image wasn't {} successfully".format(stage)


@step("waited until the image is deleted")
def wait_for_deletion(step_instance):
	sleep(IMAGE_DELETE_TIMEOUT)
