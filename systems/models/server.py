from django.db import models as django

from data.server.models import Server
from .resource import ResourceModel, ResourceModelFacadeMixin


class ServerModelFacadeMixin(ResourceModelFacadeMixin):

    def get_field_server_display(self, instance, value, short):
        return str(value)

    def get_field_servers_display(self, instance, value, short):
        servers = [ str(x) for x in value.all() ]
        return "\n".join(servers)


class ServerMixin(django.Model):

    server = django.ForeignKey(Server,
        null = True,
        on_delete = django.PROTECT,
        related_name = "%(class)s_relation",
        editable = False
    )
    class Meta:
        abstract = True

class ServerRelationMixin(django.Model):

    servers = django.ManyToManyField(Server,
        related_name = "%(class)s_relations",
        editable = False
    )
    class Meta:
        abstract = True


class ServerModel(ServerMixin, ResourceModel):

    class Meta(ResourceModel.Meta):
        abstract = True
        unique_together = ('server', 'name')
        scope = 'server'

    def __str__(self):
        return "{}:{}".format(self.server.name, self.name)

    def get_id_fields(self):
        return ('name', 'server_id')
