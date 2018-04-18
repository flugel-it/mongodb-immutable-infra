data "aws_ami" "mongodb-ubuntu" {
  most_recent = true

  filter {
    name = "name"

    values = [
      "mongodb-ubuntu-*",
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
