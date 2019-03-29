from django.db import models as django

from systems.models import environment, group, provider


class NetworkFacade(
    provider.ProviderModelFacadeMixin,
    group.GroupModelFacadeMixin,
    environment.EnvironmentModelFacadeMixin
):
    def get_field_cidr_display(self, instance, value, short):
        return value


class Network(
    provider.ProviderMixin,
    group.GroupMixin,
    environment.EnvironmentModel
):
    cidr = django.CharField(null = True, max_length = 128)

    class Meta(environment.EnvironmentModel.Meta):
        verbose_name = "network"
        verbose_name_plural = "networks"
        facade_class = NetworkFacade
        ordering = ['cidr']
        provider_name = 'network:network'
