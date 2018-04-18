resource "aws_instance" "aws-instance" {
  ami                  = "${var.os_env == "ubuntu" ? data.aws_ami.mongodb-ubuntu.id : data.aws_ami.mongodb-centos.id}"
  instance_type        = "${var.instance_type}"
  key_name             = "${var.key_name}"
  iam_instance_profile = "${aws_iam_instance_profile.cluster-join.id}"

  vpc_security_group_ids = [
    "${aws_security_group.sec_group.id}",
  ]

  subnet_id                   = "${data.aws_subnet.subnets.*.id[0]}"
  user_data                   = "${element(data.template_file.userdata.*.rendered, count.index)}"
  count                       = "${var.instance_count}"
  associate_public_ip_address = true

  root_block_device {
    delete_on_termination = true
    volume_size           = "${var.vol_size}"
    volume_type           = "gp2"
  }

  tags = "${map(
        "Name", "${var.cluster_name}-${count.index}.${var.dns_domain}",
        "Internal", "${var.cluster_name}-${count.index}.internal.${var.dns_domain}",
        "cluster", "${var.cluster_name}"
    )}"
}
