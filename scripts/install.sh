#!/usr/bin/env bash
#
# Install cluster management related packaging
#
set -e

apt-get update
apt-get install -y certbot
rm -rf /var/lib/apt/lists/*

TERRAFORM_VERSION=0.12.19
wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip 2>/dev/null
unzip -o terraform_${TERRAFORM_VERSION}_linux_amd64.zip -d /usr/local/bin

mkdir -p ~/.terraform.d/plugins
wget http://http://terraform-0.12.0-dev-snapshots.s3-website-us-west-2.amazonaws.com/terraform-provider-aws/2.7.0-dev20190415H16-dev/terraform-provider-aws_2.7.0-dev20190415H16-dev_linux_amd64.zip 2>/dev/null
unzip -o terraform-provider-aws_2.7.0-dev20190415H16-dev_linux_amd64.zip -d ~/.terraform.d/plugins
