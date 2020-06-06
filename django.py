"""
Cluster module settings definition

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
from settings.config import Config

#-------------------------------------------------------------------------------
# Core Django settings

#-------------------------------------------------------------------------------
# Addons

#
# Terraform configuration
#
TERRAFORM_MAX_PROCESSES = Config.integer('ZIMAGI_TERRAFORM_MAX_PROCESSES', 10)

#
# Ansible configuration
#
ANSIBLE_MAX_PROCESSES = Config.integer('ZIMAGI_ANSIBLE_MAX_PROCESSES', 10)
