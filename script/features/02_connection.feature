Feature: Test Connection
	Checking connection to MongoDB

	Scenario Outline: Pinging hosts
		Given server address is <host>
		When trying connect to server
		Then connection <connected> successful

		Examples:
			| host                     | connected |
			| localhost                | is        |
			| google.com               | is        |
#			| non-existing.website.com | is not    |