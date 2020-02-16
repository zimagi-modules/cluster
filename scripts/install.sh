#!/usr/bin/env bash
#
# Install cluster management related packaging
#
set -e

apt-get update
apt-get install -y certbot
rm -rf /var/lib/apt/lists/*

TERRAFORM_VERSION=0.12.19

if [ ! -f /usr/local/bin/terraform ]
then
    wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip 2>/dev/null
    unzip -o terraform_${TERRAFORM_VERSION}_linux_amd64.zip -d /usr/local/bin
fi

mkdir -p ~/.terraform.d/plugins

TERRAFORM_AWS_VERSION=2.45.0

if ! ls ~/.terraform.d/plugins/terraform-provider-aws_v${TERRAFORM_AWS_VERSION}_* 1>/dev/null 2>&1
then
    wget https://releases.hashicorp.com/terraform-provider-aws/${TERRAFORM_AWS_VERSION}/terraform-provider-aws_${TERRAFORM_AWS_VERSION}_linux_amd64.zip 2>/dev/null
    unzip -o terraform-provider-aws_${TERRAFORM_AWS_VERSION}_linux_amd64.zip -d ~/.terraform.d/plugins
fi
