Feature: Create MongoDB image
 # Enter feature description here

	@mongodb_tf
	@mongodb_image_tf
	Scenario Outline: Create images
		Given packer region is eu-west-2
		And packer AMI name is mongodb-<distribution>-test
		When validated <distribution> image
		When built <distribution> image
		Then image was created successfully

		Examples:
			| distribution |
			| ubuntu       |
			| centos       |
