from django.db import models as django

from settings.roles import Roles
from systems.models import fields, server, provider


class ServerVolumeFacade(
    provider.ProviderModelFacadeMixin,
    server.ServerModelFacadeMixin
):
    pass


class ServerVolume(
    provider.ProviderMixin,
    server.ServerModel
):
    source = django.CharField(max_length = 256)
    type = django.CharField(default = 'ext4', max_length = 128)
    owner = django.CharField(default = 'root', max_length = 128)
    group = django.CharField(default = 'root', max_length = 128)
    mode = django.CharField(default = '0755', max_length = 25)
    options = fields.CSVField()

    class Meta(server.ServerModel.Meta):
        verbose_name = "server volume"
        verbose_name_plural = "server volumes"
        facade_class = ServerVolumeFacade
        ordering = ['name']
        provider_name = 'volume'

    def __str__(self):
        return "{} ({})".format(self.server.name, self.name)

    def allowed_groups(self):
        return [ Roles.admin, Roles.server_admin ]
