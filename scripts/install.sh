#!/usr/bin/env bash
#
# Install cluster management related packaging
#
set -e

TERRAFORM_VERSION=0.12.0-beta1
wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip 2>/dev/null
unzip -o terraform_${TERRAFORM_VERSION}_linux_amd64.zip -d /usr/local/bin

mkdir -p ~/.terraform.d/plugins
wget http://terraform-0.12.0-dev-snapshots.s3-website-us-west-2.amazonaws.com/terraform-provider-aws/1.60.0-dev20190216H00-dev/terraform-provider-aws_1.60.0-dev20190216H00-dev_linux_amd64.zip 2>/dev/null
unzip -o terraform-provider-aws_1.60.0-dev20190216H00-dev_linux_amd64.zip -d ~/.terraform.d/plugins