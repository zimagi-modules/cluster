from django.db import models as django

from data.load_balancer.models import LoadBalancer
from .resource import ResourceModel, ResourceModelFacadeMixin


class LoadBalancerModelFacadeMixin(ResourceModelFacadeMixin):

    def get_field_load_balancer_display(self, instance, value, short):
        return str(value)

    def get_field_load_balancers_display(self, instance, value, short):
        load_balancers = [ str(x) for x in value.all() ]
        return "\n".join(load_balancers)


class LoadBalancerMixin(django.Model):

    load_balancer = django.ForeignKey(LoadBalancer,
        null = True,
        on_delete = django.PROTECT,
        related_name = "%(class)s_relation",
        editable = False
    )
    class Meta:
        abstract = True


class LoadBalancerRelationMixin(django.Model):

    load_balancers = django.ManyToManyField(LoadBalancer,
        related_name = "%(class)s_relation",
        editable = False
    )
    class Meta:
        abstract = True


class LoadBalancerModel(LoadBalancerMixin, ResourceModel):

    class Meta(ResourceModel.Meta):
        abstract = True
        unique_together = ('load_balancer', 'name')
        scope = 'load_balancer'

    def __str__(self):
        return "{}:{}".format(self.load_balancer.name, self.name)

    def get_id_fields(self):
        return ('name', 'load_balancer_id')
