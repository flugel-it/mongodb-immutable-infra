resource "aws_s3_bucket" "s3-terraform-state" {
  bucket        = "${var.customer}-${var.terraform_bucket_name}"
  acl           = "private"
  force_destroy = true

  tags {
    Name = "${var.customer}-${var.terraform_bucket_name}"
  }

  lifecycle {
    //        prevent_destroy = true
  }
}
