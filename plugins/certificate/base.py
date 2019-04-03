from systems.plugins import terraform


class BaseProvider(terraform.TerraformPluginProvider):

    def provider_config(self, type = None):
        self.requirement(str, 'private_key', help = 'PEM formatted private key of certificate')
        self.requirement(str, 'certificate', help = 'PEM formatted public key of certificate')
        self.option(str, 'chain', None, help = 'PEM formatted certificate chain')

    def terraform_type(self):
        return 'certificate'

    @property
    def facade(self):
        return self.command._certificate
