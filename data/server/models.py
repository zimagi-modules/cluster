from django.db import models as django

from settings.roles import Roles
from data.load_balancer_listener.models import LoadBalancerListener
from systems.models import fields, subnet, firewall, provider, load_balancer, group


class ServerFacade(
    provider.ProviderModelFacadeMixin,
    group.GroupModelFacadeMixin,
    firewall.FirewallModelFacadeMixin,
    load_balancer.LoadBalancerModelFacadeMixin,
    subnet.SubnetModelFacadeMixin
):
    def get_field_password_display(self, instance, value, short):
        if not value:
            return None

        if short:
            return self.encrypted_color('*****')
        return self.encrypted_color(value)

    def get_field_private_key_display(self, instance, value, short):
        if not value:
            return None

        if short:
            return self.encrypted_color('*****')
        return self.encrypted_color(value)

    def get_field_status_display(self, instance, value, short):
        if value == self.model.STATUS_RUNNING:
            return self.success_color(value)
        return self.error_color(value)


class Server(
    provider.ProviderMixin,
    group.GroupMixin,
    firewall.FirewallRelationMixin,
    load_balancer.LoadBalancerMixin,
    subnet.SubnetModel
):
    STATUS_RUNNING = 'running'
    STATUS_UNREACHABLE = 'unreachable'

    public_ip = django.CharField(null = True, max_length = 128)
    private_ip = django.CharField(null = True, max_length = 128)
    ssh_port = django.IntegerField(default = 22)
    user = django.CharField(null = True, max_length = 128)
    password = fields.EncryptedCharField(null = True, max_length = 1096)
    private_key = fields.EncryptedDataField(null = True)
    data_device = django.CharField(null = True, max_length = 256)
    backup_device = django.CharField(null = True, max_length = 256)

    load_balancer_listener = django.ForeignKey(LoadBalancerListener,
        null = True,
        on_delete = django.PROTECT,
        related_name = "%(class)s_relation",
        editable = False
    )
    class Meta(subnet.SubnetModel.Meta):
        verbose_name = "server"
        verbose_name_plural = "servers"
        facade_class = ServerFacade
        relation = ['load_balancer', 'load_balancer_listener']
        dynamic_fields = ['status']
        ordering = ['name']
        provider_name = 'server'

    def __str__(self):
        return "{} ({})".format(self.name, self.ip)

    @property
    def ip(self):
        return self.public_ip if self.public_ip else self.private_ip

    @property
    def status(self):
        return self.STATUS_RUNNING if self.ping() else self.STATUS_UNREACHABLE


    def allowed_groups(self):
        return [ Roles.admin, Roles.server_admin ]

    def running(self):
        if self.status == self.STATUS_RUNNING:
            return True
        return False


    def ping(self):
        return self.provider.ping()
