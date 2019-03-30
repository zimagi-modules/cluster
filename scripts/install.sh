#!/usr/bin/env bash
#
# Install cluster management related packaging
#
set -e

TERRAFORM_VERSION=0.12.0-beta1
wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip 2>/dev/null
unzip -o terraform_${TERRAFORM_VERSION}_linux_amd64.zip -d /usr/local/bin
