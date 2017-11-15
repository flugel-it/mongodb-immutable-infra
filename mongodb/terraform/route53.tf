resource "aws_route53_record" "dns_record_public" {

    zone_id = "${data.aws_route53_zone.selected.zone_id}"
    name    = "${var.cluster_name}-${count.index}.${data.aws_route53_zone.selected.name}"
    type    = "A"
    ttl     = "300"
    count   = "${var.instance_count}"
    records = ["${element(aws_instance.aws-instance.*.public_ip, count.index)}"]

}
resource "aws_route53_record" "dns_record_private" {

    zone_id = "${data.aws_route53_zone.selected.zone_id}"
    name    = "${var.cluster_name}-${count.index}.internal.${data.aws_route53_zone.selected.name}"
    type    = "A"
    ttl     = "300"
    count   = "${var.instance_count}"
    records = ["${element(aws_instance.aws-instance.*.private_ip, count.index)}"]

}
