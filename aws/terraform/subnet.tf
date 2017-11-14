# Create a subnet to launch our instances into
resource "aws_subnet" "cluster" {
  count                   = "${length(var.cidr_blocks)}"
  vpc_id                  = "${aws_vpc.cluster.id}"
  availability_zone       = "${data.aws_availability_zones.available.names[count.index]}"
  cidr_block              = "${var.cidr_blocks[count.index]}"
  map_public_ip_on_launch = true

  tags {
    "Name" = "${var.namespace}"
  }
}
