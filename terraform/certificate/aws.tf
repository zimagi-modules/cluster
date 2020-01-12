
provider "aws" {
  access_key = "${var.access_key}"
  secret_key = "${var.secret_key}"
  region = "${var.network.region}"
}

resource "aws_acm_certificate" "cert" {
  private_key      = "${var.private_key}"
  certificate_body = "${var.certificate}"
  certificate_chain = "${var.chain}"

  tags = {
    Name = "mcmi-certificate"
  }
}
output "cert_id" {
  value = "${aws_acm_certificate.cert.id}"
}
output "cert_arn" {
  value = "${aws_acm_certificate.cert.arn}"
}
