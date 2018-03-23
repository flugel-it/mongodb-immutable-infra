Feature: Create MongoDB cluster on AWS
 # Enter feature description here

	@create
	@mongodb_tf
	@mongodb_tf_create
	Scenario: Create MongoDB cluster
		Given customer name for AWS is flugel-test
		And terraform bucket name for MongoDB is terraform-state
		And AWS region for MongoDB is eu-west-2
		And terraform region for MongoDB is us-west-2
		And namespace for MongoDB is cluster_test
		And key name for MongoDB is cluster_test
		And cluster name for MongoDB is cluster_test
		And domain name for MongoDB is flugel-it.com
		And Linux distribution for MongoDB is ubuntu
		And number of instances in cluster for MongoDB is 3
		And project name for MongoDB is mongodb-cluster
		And terraform backend is set to S3 bucket
		When terraform config for MongoDB is initialized
		And terraform config for MongoDB is planned
		And terraform config for MongoDB is applied
 #		And waited until cluster is up
		Then 3 instances are created successfully
		And security group for the cluster is created and ports 22 are opened
		And IAM role with prefix cluster_test-cluster-join_ is created
 #		And port 27017 is open on all instances
