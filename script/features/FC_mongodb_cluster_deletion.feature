Feature: Delete MongoDB cluster on AWS
 # Enter feature description here

	@delete
	@mongodb_tf
	@mongodb_tf_delete
	Scenario: Delete MongoDB cluster
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
		When terraform config for MongoDB is destroyed
		Then 3 instances are deleted successfully
		And security group for the cluster is deleted
		And IAM role with prefix cluster_test-cluster-join_ is deleted

