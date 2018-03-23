Feature: Deleting S3 bucket for terraform state configuration

	@delete
	@mongodb_tf
	@aws_structure_tf
	@s3_tf
	Scenario: Deleting state bucket
		Given customer name for S3 is flugel-test
		And terraform bucket name for S3 is terraform-state
		And AWS region for S3 is us-west-2
		And S3 bucket called flugel-test-terraform-state is created
		When terraform config for S3 is destroyed
		Then S3 bucket called flugel-test-terraform-state is deleted
