Feature: Deploying MongoDB
	This test installs MongoDB using Ansible and checks
	if port with Mongodb is available

	@check
	Scenario: Installing MongoDB on Ubuntu
		Given file with Ansible configuration
		And checked if file exists
		When Ansible deployment passed
		Then MongoDB is available at port 8090