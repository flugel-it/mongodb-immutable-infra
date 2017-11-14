# Create an IAM role for the auto-join
resource "aws_iam_role" "cluster-join" {
  name_prefix        = "${var.namespace}-cluster-join_"
  assume_role_policy = "${file("${path.module}/files/roles/assume-role.json")}"
}

# Create the policy
resource "aws_iam_policy" "cluster-join" {
  name_prefix = "${var.namespace}-cluster-join_"
  description = "Allows Consul nodes to describe instances for joining."
  policy      = "${file("${path.module}/files/roles/describe-instances.json")}"

  lifecycle {
    create_before_destroy = true
  }
}

# Attach the policy
resource "aws_iam_policy_attachment" "cluster-join" {
  name       = "${var.namespace}-cluster-join"
  roles      = ["${aws_iam_role.cluster-join.name}"]
  policy_arn = "${aws_iam_policy.cluster-join.arn}"
}

# Create the instance profile
resource "aws_iam_instance_profile" "cluster-join" {
  name_prefix = "${var.namespace}-cluster-join_"
  role        = "${aws_iam_role.cluster-join.name}"
}
