variable "aws_region" {
  description = "AWS region to create the environment"
}

variable "namespace" {}

variable "vpc_cidr_block" {
  description = "The top-level CIDR block for the VPC."
}

variable "cidr_blocks" {
  description = "The CIDR blocks to create the workstations in."
  type = "list"
}

variable "public_key_path" {}
