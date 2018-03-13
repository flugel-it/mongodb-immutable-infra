from lettuce import step, world

# world.tf_configs = CONFIG_TEMPLATE.copy()
world.tf_configs = {}
world.tf_init_configs = {}


@step("customer name for (S3|AWS|MongoDb) is ([A-Za-z0-9\-_]*)")
def get_customer_name(step_instance, namespace, customer):
	world.tf_configs['customer'] = customer


@step("terraform bucket name for (S3|AWS|MongoDb) is ([A-Za-z0-9\-_]*)")
def get_terraform_name(step_instance, namespace, bucket):
	world.tf_configs['terraform_bucket_name'] = bucket


@step("AWS region for (S3|AWS|MongoDb) is ([a-z]{2}-[a-z]+-[1-9])")
def get_aws_region(step_instance, namespace, aws_region):
	world.tf_configs['aws_region'] = aws_region


@step("namespace for (S3|AWS|MongoDb) is ([A-Za-z0-9\-_]*)")
def get_customer_name(step_instance, namespace, ns):
	world.tf_configs['namespace'] = ns


@step("project name for (S3|AWS|MongoDb) is ([A-Za-z0-9\-_]*)")
def get_customer_name(step_instance, namespace, project_name):
	world.tf_configs['project_name'] = project_name


@step("public key path for (S3|AWS|MongoDb) is (\S+)")
def get_customer_name(step_instance, namespace, path):
	world.tf_configs['public_key_path'] = path


@step("terraform region for (S3|AWS|MongoDb) is ([a-z]{2}-[a-z]+-[1-9])")
def get_aws_region(step_instance, namespace, aws_region):
	world.tf_region = aws_region


@step("terraform backend is set to S3 bucket")
def step_impl(step_instance):
	world.tf_init_configs = {
		"bucket": "{}-{}".format(world.tf_configs['customer'], world.tf_configs['terraform_bucket_name']),
		"key": "{}/terraform.tfstate".format(world.tf_configs["project_name"]),
		"region": world.tf_region,
	}
