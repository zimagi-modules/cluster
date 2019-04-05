from django.conf import settings

from systems.plugins import meta, terraform

import datetime


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

    def prepare_instance(self, instance, created):
        super().prepare_instance(instance, created)
        ca = self.get_certificate_authority(instance)
        if ca:
            if created or not instance.certificate_updated:
                ca.request()
            else:
                start = instance.certificate_updated.date()
                now = datetime.datetime.now().date()
                days = (now - start).days

                if days >= instance.valid_days:
                    ca.renew()

    def finalize_terraform(self, instance):
        if not self.test:
            ca = self.get_certificate_authority(instance)
            if ca:
                ca.revoke()

        super().finalize_terraform(instance)


class DomainRecordProvider(terraform.TerraformPluginProvider):

    def terraform_type(self):
        return 'domain_record'

    @property
    def facade(self):
        return self.command._domain_record


class BaseProvider(meta.MetaPluginProvider):

    def register_types(self):
        self.set('domain', DomainProvider)
        self.set('domain_record', DomainRecordProvider)
