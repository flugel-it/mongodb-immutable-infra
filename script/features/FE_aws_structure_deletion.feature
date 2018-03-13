Feature: Deleting AWS structure used for MongoDB
 # Enter feature description here

	@mongodb_tf
	@mongodb_image_tf
	@aws_structure_tf
	Scenario: Delete AWS structure for MongoDB
		Given customer name for AWS is flugel-test
		And terraform bucket name for AWS is terraform-state
		And AWS region for AWS is eu-west-1
		And AWS region for AWS is us-west-2
		And namespace for AWS is Testing
		And public key path for AWS is ~/.ssh/id_rsa.pub
		When terraform config for AWS is destroyed
