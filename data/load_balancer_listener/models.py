from django.db import models as django

from data.certificate.models import Certificate
from systems.models import base, fields, load_balancer, provider


class LoadBalancerListenerFacade(
    provider.ProviderModelFacadeMixin,
    load_balancer.LoadBalancerModelFacadeMixin
):
    pass


class LoadBalancerListener(
    provider.ProviderMixin,
    load_balancer.LoadBalancerModel
):
    port = django.IntegerField(null = True)
    target_port = django.IntegerField(null = True)

    health_check_path = django.CharField(null = True, max_length = 255, default = '/')
    health_check_interval = django.IntegerField(default = 30)
    health_check_timeout = django.IntegerField(default = 10)

    healthy_status = fields.CSVField(default = '200')
    healthy_threshold = django.IntegerField(default = 3)
    unhealthy_threshold = django.IntegerField(default = 3)

    certificate = django.ForeignKey(Certificate,
        null = True,
        on_delete = django.PROTECT,
        related_name = "%(class)s_relation",
        editable = False
    )
    class Meta(load_balancer.LoadBalancerModel.Meta):
        verbose_name = "load balancer listener"
        verbose_name_plural = "load balancer listeners"
        facade_class = LoadBalancerListenerFacade
        relation = 'certificate'
        ordering = ['name']
        provider_name = 'load_balancer:load_balancer_listener'
        provider_relation = 'load_balancer'
        command_base = 'lb listener'

    def __str__(self):
        return "{}".format(self.name)
