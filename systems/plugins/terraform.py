from django.conf import settings

from .data import DataProviderState, DataPluginProvider
from utility.terraform import Terraform

import os
import json


class TerraformWrapper(object):

    def __init__(self, provider, instance):
        self.provider = provider
        self.manager = provider.command.manager
        self.instance = instance
        self.terraform = None

        if self.provider.terraform_type():
            self.terraform = Terraform(
                self.provider.command,
                self.provider.terraform_type(),
                self.instance.get_id()
            )


    def plan(self):
        if self.provider.terraform_type():
            manifest_path = self._get_manifest_path()
            if manifest_path:
                variables = self.provider.get_variables(self.instance)
                self.provider.command.data('variables', json.dumps(variables, indent=2))
                self.terraform.plan(manifest_path, variables, self.instance.state_config)

    def apply(self):
        if self.provider.terraform_type():
            manifest_path = self._get_manifest_path()
            if manifest_path:
                variables = self.provider.get_variables(self.instance)
                self.instance.state_config = self.terraform.apply(manifest_path, variables, self.instance.state_config)

    def destroy(self):
        if self.provider.terraform_type():
            manifest_path = self._get_manifest_path()
            if manifest_path:
                variables = self.provider.get_variables(self.instance)
                self.terraform.destroy(manifest_path, variables, self.instance.state_config)


    def _get_manifest_path(self):
        try:
            name = getattr(self.instance, 'terraform_name', self.instance.provider_type)
            return self.manager.module_file(
                'terraform',
                self.provider.terraform_type(),
                "{}.tf".format(name)
            )
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

    def terraform_lock_id(self):
        # Override in subclass
        return None


    def add_credentials(self, config):
        # Override in subclass
        pass

    def remove_credentials(self, config):
        # Override in subclass
        pass


    def get_terraform(self, instance):
        if not getattr(self, '_terraform_cache', None):
            self._terraform_cache = TerraformWrapper(self, instance)
        return self._terraform_cache


    def initialize_instance(self, instance, created):
        terraform = self.get_terraform(instance)

        self.add_credentials(instance.config)

        def initialize():
            self.initialize_terraform(instance, created)

        self.run_exclusive(self.terraform_lock_id(), initialize)

        if self.test:
            terraform.plan()
        else:
            terraform.apply()


    def initialize_terraform(self, instance, created):
        # Override in subclass
        pass

    def prepare_instance(self, instance, created):
        super().prepare_instance(instance, created)
        self.remove_credentials(instance.config)

    def finalize_instance(self, instance):
        self.add_credentials(instance.config)
        self.finalize_terraform(instance)
        self.get_terraform(instance).destroy()
        self.remove_credentials(instance.config)

    def finalize_terraform(self, instance):
        # Override in subclass
        pass
