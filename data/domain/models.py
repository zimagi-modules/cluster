from django.db import models as django

from systems.models import environment, group, provider


class DomainFacade(
    provider.ProviderModelFacadeMixin,
    group.GroupModelFacadeMixin,
    environment.EnvironmentModelFacadeMixin
):
    pass


class Domain(
    provider.ProviderMixin,
    group.GroupMixin,
    environment.EnvironmentModel
):
    class Meta(environment.EnvironmentModel.Meta):
        verbose_name = "domain"
        verbose_name_plural = "domains"
        facade_class = DomainFacade
        provider_name = 'domain:domain'

    def __str__(self):
        return "{}".format(self.name)
