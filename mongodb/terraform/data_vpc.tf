data "aws_vpc" "consul" {

    tags {
        Name = "${var.namespace}"
    }

}
