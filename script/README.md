# Tests for MongoDB II

> **Info:**  
> These tests won't work on Windows

To run tests for certain category of tests you should run:
```bash
lettuce -t TAG_NAME
```
Where TAG_NAME is one of these:
 * `s3_tf` - tests for S3 bucket
 * `aws_structure_tf` - tests for AWS structure
 * `mongodb_image_tf` - tests for MongoDB making images with packer
 * `mongodb_tf` - tests for MongoDB clusters