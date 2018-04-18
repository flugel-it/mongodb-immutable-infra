data "aws_ami" "mongodb-centos" {
  most_recent = true

  filter {
    name = "name"

    values = [
      "mongodb-centos-*",
    ]
  }

  filter {
    name = "virtualization-type"

    values = [
      "hvm",
    ]
  }

  owners = [
    "${data.aws_caller_identity.current.account_id}",
  ]
}
