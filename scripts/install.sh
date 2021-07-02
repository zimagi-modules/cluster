#!/usr/bin/env bash
#
# Install cluster management related packaging
#
set -e

apt-get update
apt-get install -y certbot sshpass openssh-server
rm -rf /var/lib/apt/lists/*

TERRAFORM_VERSION=1.0.1

if [ ! -f /usr/local/bin/terraform ]
then
    wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip 2>/dev/null
    unzip -o terraform_${TERRAFORM_VERSION}_linux_amd64.zip -d /usr/local/bin
fi
mkdir -p ~/.terraform.d/plugins
