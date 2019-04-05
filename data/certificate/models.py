from django.db import models as django

from systems.models import network, group, provider, fields


class CertificateFacade(
    provider.ProviderModelFacadeMixin,
    group.GroupModelFacadeMixin,
    network.NetworkModelFacadeMixin
):
    def get_field_private_key_display(self, instance, value, short):
        return self.encrypted_color(value)

    def get_field_certificate_display(self, instance, value, short):
        return self.encrypted_color(value)

    def get_field_chain_display(self, instance, value, short):
        return self.encrypted_color(value)


class Certificate(
    provider.ProviderMixin,
    group.GroupMixin,
    network.NetworkModel
):
    private_key = fields.EncryptedDataField(null = True)
    certificate = fields.EncryptedDataField(null = True)
    chain = fields.EncryptedDataField(null = True)

    class Meta(network.NetworkModel.Meta):
        verbose_name = "certificate"
        verbose_name_plural = "certificates"
        facade_class = CertificateFacade
        provider_name = 'certificate'

    def __str__(self):
        return "{}".format(self.name)
