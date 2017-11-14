resource "aws_key_pair" "consul" {
  key_name   = "${var.namespace}"
  public_key = "${file("${var.public_key_path}")}"
}
