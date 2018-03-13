from lettuce import step

from utils import check_if_bucket_exists


@step("S3 bucket called ([A-Za-z0-9\-_]*) is (created|deleted)")
def check_bucket_state(step_instance, full_bucket_name, state):
	exists = check_if_bucket_exists(full_bucket_name)
	if state == "created":
		assert exists, "The bucket called {} is not created".format(full_bucket_name)
	elif state == "deleted":
		assert not exists, "The bucket called {} is not deleted".format(full_bucket_name)
	else:
		assert False, "Such state doesn't exist"
