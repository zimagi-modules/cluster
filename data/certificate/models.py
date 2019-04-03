from django.db import models as django

from systems.models import environment, group, provider, fields


class CertificateFacade(
    provider.ProviderModelFacadeMixin,
    group.GroupModelFacadeMixin,
    environment.EnvironmentModelFacadeMixin
):
    def get_field_private_key_display(self, instance, value, short):
        return value

    def get_field_certificate_display(self, instance, value, short):
        return value

    def get_field_chain_display(self, instance, value, short):
        return value


class Certificate(
    provider.ProviderMixin,
    group.GroupMixin,
    environment.EnvironmentModel
):
    private_key = fields.EncryptedDataField(null = True)
    certificate = fields.EncryptedDataField(null = True)
    chain = fields.EncryptedDataField(null = True)

    class Meta(environment.EnvironmentModel.Meta):
        verbose_name = "certificate"
        verbose_name_plural = "certificates"
        facade_class = CertificateFacade
        provider_name = 'certificate'

    def __str__(self):
        return "{}".format(self.name)
