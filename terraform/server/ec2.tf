
provider "aws" {
  access_key = "${var.access_key}"
  secret_key = "${var.secret_key}"
  region = "${var.subnet.network.region}"
}

resource "aws_instance" "server" {
  subnet_id = "${var.subnet.subnet_id}"
  ami = "${var.image}"
  instance_type = "${var.machine}"
  tenancy = "${var.tenancy}"
  ebs_optimized = "${var.ebs_optimized}"
  monitoring = "${var.monitoring}"
  associate_public_ip_address = "${var.use_public_ip}"

  key_name = "${var.key_name}"
  vpc_security_group_ids = "${var.security_groups}"

  root_block_device {
    delete_on_termination = "true"
    volume_size = 8
    volume_type = "${var.ebs_type}"
    iops = "${var.ebs_iops}"
  }

  tags = {
    Name = "cenv-compute"
  }
}
output "instance_id" {
  value = "${aws_instance.server.id}"
}
output "private_ip_address" {
  value = "${aws_instance.server.private_ip}"
}
output "public_ip_address" {
  value = "${aws_instance.server.public_ip}"
}

resource "aws_ebs_volume" "data" {
  availability_zone = "${aws_instance.server.availability_zone}"
  size = "${var.ebs_size}"
  type = "${var.ebs_type}"
  iops = "${var.ebs_iops}"
  encrypted = "${var.ebs_encrypted}"

  tags = {
    Name = "cenv-compute"
  }
}
output "data_volume_id" {
  value = "${aws_ebs_volume.data.id}"
}

resource "aws_volume_attachment" "data" {
  device_name = "${var.data_device}"
  volume_id = "${aws_ebs_volume.data.id}"
  instance_id = "${aws_instance.server.id}"
}

resource "aws_lb_target_group_attachment" "gateway" {
  count = "${var.load_balancer_listener != null ? 1 : 0}"
  target_group_arn = "${var.load_balancer_listener.target_group_arn}"
  target_id = "${aws_instance.server.id}"
}
