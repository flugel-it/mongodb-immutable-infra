resource "aws_route53_record" "dns_record" {

    zone_id = "${data.aws_route53_zone.selected.zone_id}"
    name    = "${var.cluster_name}-${count.index}.${data.aws_route53_zone.selected.name}"
    type    = "A"
    ttl     = "300"
    count   = "${var.instance_count}"
    records = ["${element(aws_instance.aws-instance.*.private_ip, count.index)}"]

}
