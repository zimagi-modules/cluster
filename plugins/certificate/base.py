from systems.plugins import terraform


class BaseProvider(terraform.TerraformPluginProvider):

    def terraform_type(self):
        return 'certificate'

    @property
    def facade(self):
        return self.command._certificate

    def initialize_terraform(self, instance, created):
        if instance.domain:
            instance.private_key = instance.domain.private_key
            instance.certificate = instance.domain.certificate
            instance.chain = instance.domain.fullchain

        super().initialize_terraform(instance, created)
