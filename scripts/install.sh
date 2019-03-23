#!/usr/bin/env bash
#
# Install cluster management related packaging
#
set -e

TERRAFORM_VERSION=0.12.0-alpha4
wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_terraform_${TERRAFORM_VERSION}_linux_amd64.zip
unzip terraform_${TERRAFORM_VERSION}_terraform_${TERRAFORM_VERSION}_linux_amd64.zip -d /usr/local/bin
