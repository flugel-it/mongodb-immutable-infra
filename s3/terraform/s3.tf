resource "aws_s3_bucket" "s3-terraform-state" {
    bucket = "${var.customer}-${var.terraform_bucket_name}"
    acl = "private"

    tags {
        Name = "${var.customer}-${var.terraform_bucket_name}"
    }

    lifecycle {
        //        prevent_destroy = true
    }
}
