data "aws_subnet_ids" "subnet" {
  vpc_id = "${data.aws_vpc.consul.id}"
}

data "aws_subnet" "subnets" {
  count = "${length(data.aws_subnet_ids.subnet.ids)}"
  id = "${data.aws_subnet_ids.subnet.ids[count.index]}"
  /*default_for_az = true*/
}
