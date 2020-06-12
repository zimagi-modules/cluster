from django.conf import settings

from systems.plugins.index import BasePlugin

import datetime


class DomainBaseProvider(BasePlugin('domain.domain')):

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
