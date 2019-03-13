"""
Django settings for the System administrative interface

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
from utility.config import Config

#-------------------------------------------------------------------------------
# Core Django settings

#
# Applications and libraries
#
INSTALLED_APPS = [
    'interface',
    'data.network',
    'data.subnet',
    'data.firewall',
    'data.firewall_rule',
    'data.storage',
    'data.storage_mount',
    'data.server'
]

#-------------------------------------------------------------------------------
# Django Addons

#-------------------------------------------------------------------------------
# Cloud configurations

#
# Supported federation providers
#
FEDERATION_PROVIDERS = {
    'internal': 'systems.federation.Internal'
}
for name, cls_str in Config.dict('FEDERATION_PROVIDERS').items():
    FEDERATION_PROVIDERS[name] = cls_str

#
# Supported network providers
#
NETWORK_PROVIDERS = {
    'internal': 'systems.network.Internal',
    'aws': 'systems.network.AWS'
}
for name, cls_str in Config.dict('NETWORK_PROVIDERS').items():
    NETWORK_PROVIDERS[name] = cls_str

#
# Supported storage providers
#
STORAGE_PROVIDERS = {
    'internal': 'systems.storage.Internal',
    'efs': 'systems.storage.AWSEFS'
}
for name, cls_str in Config.dict('STORAGE_PROVIDERS').items():
    STORAGE_PROVIDERS[name] = cls_str

#
# Supported server providers
#
SERVER_PROVIDERS = {
    'internal': 'systems.compute.Internal',
    'ec2': 'systems.compute.AWSEC2'
}
for name, cls_str in Config.dict('SERVER_PROVIDERS').items():
    SERVER_PROVIDERS[name] = cls_str

#-------------------------------------------------------------------------------
# Indexes

#
# Provider type index
#
PROVIDER_INDEX = {
    'federation': {
        'registry': FEDERATION_PROVIDERS,
        'base': 'systems.federation.BaseFederationProvider'
    },
    'network': {
        'registry': NETWORK_PROVIDERS,
        'base': 'systems.network.BaseNetworkProvider'
    },
    'storage': {
        'registry': STORAGE_PROVIDERS,
        'base': 'systems.storage.BaseStorageProvider'
    },
    'server': {
        'registry': SERVER_PROVIDERS,
        'base': 'systems.compute.BaseComputeProvider'
    }
}
