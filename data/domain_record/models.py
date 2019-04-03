from django.db import models as django

from systems.models import base, domain, provider, fields


class DomainRecordFacade(
    provider.ProviderModelFacadeMixin,
    domain.DomainModelFacadeMixin
):
    def get_field_type_display(self, instance, value, short):
        return value

    def get_field_target_display(self, instance, value, short):
        return value

    def get_field_ttl_display(self, instance, value, short):
        return str(value)

    def get_field_values_display(self, instance, value, short):
        return "\n".join(value)


class DomainRecord(
    provider.ProviderMixin,
    domain.DomainModel
):
    type = django.CharField(max_length = 10, default = 'A', choices = base.format_choices(
        'A', 'AAAA', 'CAA', 'CNAME', 'MX', 'NAPTR', 'NS', 'PTR', 'SOA', 'SPF', 'SRV', 'TXT'
    ))
    target = django.CharField(null = True, max_length = 255)
    ttl = django.IntegerField(default = 300)
    values = fields.EncryptedDataField(default = [])

    class Meta(domain.DomainModel.Meta):
        verbose_name = "domain record"
        verbose_name_plural = "domain records"
        facade_class = DomainRecordFacade
        provider_name = 'domain:domain_record'
        provider_relation = 'domain'

    def __str__(self):
        return "{}".format(self.name)
