from django.conf import settings

from .data import DataProviderState, DataPluginProvider
from utility.terraform import Terraform

import os
import json


class TerraformWrapper(object):

    def __init__(self, provider, id):
        self.provider = provider
        self.manager = provider.command.manager
        self.terraform = Terraform(provider.command, id)

    def plan(self, type, instance):
        if type:
            manifest_name = getattr(instance, 'terraform_name', instance.provider_type)
            manifest_path = self._get_manifest_path(type, manifest_name)
            if manifest_path:
                variables = self.provider.get_variables(instance)
                self.provider.command.data('variables', json.dumps(variables, indent=2))
                self.terraform.plan(manifest_path, variables, instance.state_config)

    def apply(self, type, instance):
        if type:
            manifest_name = getattr(instance, 'terraform_name', instance.provider_type)
            manifest_path = self._get_manifest_path(type, manifest_name)
            if manifest_path:
                variables = self.provider.get_variables(instance)
                instance.state_config = self.terraform.apply(manifest_path, variables, instance.state_config)

    def destroy(self, type, instance):
        if type:
            manifest_name = getattr(instance, 'terraform_name', instance.provider_type)
            manifest_path = self._get_manifest_path(type, manifest_name)
            if manifest_path:
                variables = self.provider.get_variables(instance)
                self.terraform.destroy(manifest_path, variables, instance.state_config)

    def _get_manifest_path(self, type, name):
        try:
            return self.manager.module_file('terraform', type, "{}.tf".format(name))
        except Exception as e:
            return None


class TerraformState(DataProviderState):

    @property
    def variables(self):
        variables = {}
        outputs = self.get('outputs')

        if outputs:
            for key, info in outputs.items():
                variables[key] = info['value']

        return variables


class TerraformPluginProvider(DataPluginProvider):

    def provider_state(self):
        return TerraformState

    def terraform_type(self):
        # Override in subclass
        return None


    def add_credentials(self, config):
        # Override in subclass
        pass

    def remove_credentials(self, config):
        # Override in subclass
        pass


    def terraform(self, id):
        if not getattr(self, '_terraform_cache', None):
            self._terraform_cache = TerraformWrapper(self, id)
        return self._terraform_cache


    def initialize_instance(self, instance, created):
        self.add_credentials(instance.config)
        self.initialize_terraform(instance, created)

        if self.test:
            self.terraform(instance.id).plan(self.terraform_type(), instance)
        else:
            self.terraform(instance.id).apply(self.terraform_type(), instance)

    def initialize_terraform(self, instance, created):
        # Override in subclass
        pass

    def prepare_instance(self, instance, created):
        super().prepare_instance(instance, created)
        self.remove_credentials(instance.config)

    def finalize_instance(self, instance):
        self.add_credentials(instance.config)
        self.finalize_terraform(instance)
        self.terraform(instance.id).destroy(self.terraform_type(), instance)

    def finalize_terraform(self, instance):
        # Override in subclass
        pass
