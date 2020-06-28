from django.conf import settings

from plugins import data
from utility.terraform import Terraform
from utility.runtime import Runtime

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
                variables = self.provider.get_variables(self.instance, True)
                if Runtime.debug():
                    self.provider.command.warning("{}: {}".format(
                        self.instance.name,
                        json.dumps(variables, indent = 2)
                    ))
                self.provider.command.data('variables', json.dumps(variables, indent=2))
                self.terraform.plan(manifest_path, variables, self.instance.state_config)

    def apply(self):
        if self.provider.terraform_type():
            manifest_path = self._get_manifest_path()
            if manifest_path:
                variables = self.provider.get_variables(self.instance, True)
                if Runtime.debug():
                    self.provider.command.warning("{}: {}".format(
                        self.instance.name,
                        json.dumps(variables, indent = 2)
                    ))
                self.instance.state_config = self.terraform.apply(manifest_path, variables, self.instance.state_config)

    def destroy(self):
        if self.provider.terraform_type():
            manifest_path = self._get_manifest_path()
            if manifest_path:
                variables = self.provider.get_variables(self.instance, True)
                if Runtime.debug():
                    self.provider.command.warning("{}: {}".format(
                        self.instance.name,
                        json.dumps(variables, indent = 2)
                    ))
                self.terraform.destroy(manifest_path, variables, self.instance.state_config)


    def _get_manifest_path(self):
        try:
            name = getattr(self.instance, 'terraform_name', self.instance.provider_type)
            return self.manager.index.get_module_file(
                'terraform',
                self.provider.terraform_type(),
                "{}.tf".format(name)
            )
        except Exception as e:
            return None


class TerraformState(data.DataProviderState):

    @property
    def variables(self):
        variables = {}
        outputs = self.get('outputs')

        if outputs:
            for key, info in outputs.items():
                variables[key] = info['value']

        return variables


class BasePlugin(data.BasePlugin):

    @classmethod
    def generate(cls, plugin, generator):
        super().generate(plugin, generator)

        def terraform_type(self):
            if 'manifest' in generator.spec:
                return generator.spec['manifest']
            return generator.spec['data']

        if not getattr(plugin, 'terraform_type', None):
            plugin.terraform_type = terraform_type


    def provider_state(self):
        return TerraformState


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
        self.initialize_terraform(instance, created)

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
