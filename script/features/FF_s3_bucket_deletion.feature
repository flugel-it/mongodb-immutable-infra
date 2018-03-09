Feature: Deleting S3 bucket for terraform state configuration

	@mongodb_tf
	@mongodb_image_tf
	@aws_structure_tf
	@s3_tf
	Scenario: Deleting state bucket
		Given customer name flugel-test
		And terraform bucket name terraform-state
		And AWS region us-west-2
		And S3 bucket called flugel-test-terraform-state is created
		When terraform config is destroyed
		Then S3 bucket called flugel-test-terraform-state is deleted
