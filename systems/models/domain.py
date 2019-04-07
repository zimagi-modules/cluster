from django.db import models as django

from data.domain.models import Domain
from .resource import ResourceModel, ResourceModelFacadeMixin


class DomainModelFacadeMixin(ResourceModelFacadeMixin):

    def get_field_domain_display(self, instance, value, short):
        return str(value)

    def get_field_domains_display(self, instance, value, short):
        domains = [ str(x) for x in value.all() ]
        return "\n".join(domains)


class DomainMixin(django.Model):

    domain = django.ForeignKey(Domain,
        null = True,
        on_delete = django.PROTECT,
        related_name = "%(class)s_relation",
        editable = False
    )
    class Meta:
        abstract = True

class DomainRelationMixin(django.Model):

    domains = django.ManyToManyField(Domain,
        related_name = "%(class)s_relations",
        editable = False
    )
    class Meta:
        abstract = True


class DomainModel(DomainMixin, ResourceModel):

    class Meta(ResourceModel.Meta):
        abstract = True
        unique_together = ('domain', 'name')
        scope = 'domain'

    def __str__(self):
        return "{}:{}".format(self.domain.name, self.name)

    def get_id_fields(self):
        return ('name', 'domain_id')
