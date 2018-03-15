Feature: Deleting AWS structure used for MongoDB
 # Enter feature description here

	@mongodb_tf
	@aws_structure_tf
	Scenario: Delete AWS structure for MongoDB
		Given customer name for AWS is flugel-test
		And terraform bucket name for AWS is terraform-state
		And AWS region for AWS is eu-west-2
		And terraform region for S3 is us-west-2
		And namespace for AWS is cluster_automation_test
		And project name for AWS is aws-vpc
		And public key path for AWS is ~/.ssh/id_rsa.pub
		And VPC with name cluster_automation_test is exists
		When terraform config for AWS is destroyed
		Then VPC with name cluster_automation_test is doesn't exist
