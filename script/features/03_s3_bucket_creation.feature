Feature: Creating S3 bucket for terraform state configuration

	@create
	@mongodb_tf
	@aws_structure_tf
	@s3_tf
	Scenario: Creating state bucket
		Given customer name for S3 is flugel-test
		And terraform bucket name for S3 is terraform-state
		And AWS region for S3 is us-west-2
		And S3 bucket called flugel-test-terraform-state is deleted
		When terraform config for S3 is initialized
		And terraform config for S3 is planned
		And terraform config for S3 is applied
		Then S3 bucket called flugel-test-terraform-state is created