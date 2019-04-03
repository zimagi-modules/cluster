
provider "aws" {
  access_key = "${var.access_key}"
  secret_key = "${var.secret_key}"
  region = "${var.region}"
}

resource "aws_route53_zone" "main" {
  name = "${var.name}"
  force_destroy = true

  tags = {
    Name = "cenv-domain"
  }
}
output "zone_id" {
  value = "${aws_route53_zone.main.id}"
}
output "zone_name_servers" {
  value = "${aws_route53_zone.main.name_servers}"
}
