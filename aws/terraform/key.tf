resource "aws_key_pair" "key" {
  key_name   = "${var.namespace}"
  public_key = "${file("${var.public_key_path}")}"
}
