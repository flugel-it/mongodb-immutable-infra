data "template_file" "userdata" {
  count    = "${var.instance_count}"
  template = "${file("${path.module}/files/userdata.sh.tpl")}"

  vars {
    HOSTNAME     = "${var.cluster_name}-${count.index}.${var.dns_domain}"
    CLUSTER_NAME = "${var.cluster_name}"
  }
}
