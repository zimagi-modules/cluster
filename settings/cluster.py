"""
Cluster module settings definition

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
from .config import Config

#-------------------------------------------------------------------------------
# Core Django settings

#-------------------------------------------------------------------------------
# Addons

#
# Terraform configuration
#
TERRAFORM_MAX_PROCESSES = Config.integer('CENV_TERRAFORM_MAX_PROCESSES', 1)
