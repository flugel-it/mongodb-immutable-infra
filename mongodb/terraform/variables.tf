variable "instance_type" {}
variable "instance_count" {}
variable "image_owner" {}
variable "os_env" {
    description = "OS environment"
}
variable "tf_region" {}
variable "key_name" {}
variable "project_name" {}
variable "aws_region" {
    description = "The region where AWS operations will take place"
}
variable "dns_domain" {}
variable "cluster_name" {}
variable "vol_size" {}
variable "customer" {
    description = "Customer name (one word)"
}
variable "consul_join_tag_key" {
  description = "The key of the tag to auto-jon on EC2."
}

variable "consul_join_tag_value" {
  description = "The value of the tag to auto-join on EC2."
}
variable "namespace" {}
