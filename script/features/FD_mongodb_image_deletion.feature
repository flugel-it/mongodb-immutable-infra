Feature: Delete MongoDB image
 # Enter feature description here

	@mongodb_tf
	@mongodb_image_tf
	Scenario Outline: Delete images
		Given packer region is eu-west-2
		And packer AMI name is mongodb-<distribution>-test
		When deleted <distribution> image
		And waited until the image is deleted
		Then image was deleted successfully

		Examples:
			| distribution |
			| ubuntu       |
			| centos       |
