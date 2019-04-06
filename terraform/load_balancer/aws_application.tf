
provider "aws" {
  access_key = "${var.access_key}"
  secret_key = "${var.secret_key}"
  region = "${var.network.region}"
}

resource "aws_lb" "main" {
  load_balancer_type = "application"
  name = "${var.name}"
  internal = "${var.internal}"
  idle_timeout = "${var.idle_timeout}"

  subnets = "${var.subnets}"
  security_groups = "${var.security_groups}"

  enable_http2 = true
  enable_cross_zone_load_balancing = true

  tags = {
    Name = "cenv-load-balancer"
  }
}
output "lb_id" {
  value = "${aws_lb.main.id}"
}
output "lb_arn" {
  value = "${aws_lb.main.arn}"
}
output "lb_dns_name" {
  value = "${aws_lb.main.dns_name}"
}