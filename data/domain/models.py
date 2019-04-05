from django.db import models as django

from systems.models import environment, group, provider, fields


class DomainFacade(
    provider.ProviderModelFacadeMixin,
    group.GroupModelFacadeMixin,
    environment.EnvironmentModelFacadeMixin
):
    def get_field_private_key_display(self, instance, value, short):
        return self.encrypted_color(value)

    def get_field_certificate_display(self, instance, value, short):
        return self.encrypted_color(value)

    def get_field_chain_display(self, instance, value, short):
        return self.encrypted_color(value)

    def get_field_fullchain_display(self, instance, value, short):
        return self.encrypted_color(value)


class Domain(
    provider.ProviderMixin,
    group.GroupMixin,
    environment.EnvironmentModel
):
    email = django.CharField(null = True, max_length = 255)

    certificate_authority = django.CharField(null = True, max_length = 255)
    certificate_updated = django.DateTimeField(null = True, editable = False)

    private_key = fields.EncryptedDataField(null = True)
    certificate = fields.EncryptedDataField(null = True)
    chain = fields.EncryptedDataField(null = True)
    fullchain = fields.EncryptedDataField(null = True)

    class Meta(environment.EnvironmentModel.Meta):
        verbose_name = "domain"
        verbose_name_plural = "domains"
        facade_class = DomainFacade
        provider_name = 'domain:domain'

    def __str__(self):
        return "{}".format(self.name)
