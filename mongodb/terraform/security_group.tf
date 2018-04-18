resource "aws_security_group" "sec_group" {
  name        = "${var.customer}-${var.project_name}-security-group"
  description = "Allow every internal traffic"
  vpc_id      = "${data.aws_vpc.consul.id}"

  ingress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"

    cidr_blocks = [
      "${data.aws_subnet.subnets.*.cidr_block}",
    ]
  }

  ingress {
    from_port = "22"
    to_port   = "22"
    protocol  = "tcp"

    cidr_blocks = [
      "0.0.0.0/0",
    ]
  }

  egress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"

    cidr_blocks = [
      "0.0.0.0/0",
    ]
  }

  tags {
    Name = "${var.customer}-${var.project_name}-security-group"
  }
}
