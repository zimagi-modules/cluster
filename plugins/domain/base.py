from django.conf import settings

from systems.plugins import meta, terraform


class DomainProvider(terraform.TerraformPluginProvider):

    def terraform_type(self):
        return 'domain'

    @property
    def facade(self):
        return self.command._domain

    def get_certificate_authority(self, instance):
        if instance.certificate_authority:
            return self.command.get_provider(
                'certificate_authority',
                instance.certificate_authority,
                instance
            )
        return None


class DomainRecordProvider(terraform.TerraformPluginProvider):

    def provider_config(self, type = None):
        self.option(str, 'target', None, help = 'DNS record target domain name')
        self.option(str, 'type', 'A', help = 'DNS record type')
        self.option(int, 'ttl', 300, help = 'DNS time to live (secs)')
        self.option(list, 'values', [], help = 'DNS record values')

    def terraform_type(self):
        return 'domain_record'

    @property
    def facade(self):
        return self.command._domain_record


class BaseProvider(meta.MetaPluginProvider):

    def register_types(self):
        self.set('domain', DomainProvider)
        self.set('domain_record', DomainRecordProvider)
