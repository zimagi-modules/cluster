from settings.roles import Roles
from .network import NetworkRouterCommand, NetworkActionCommand
from systems.command.mixins import load_balancer


class LoadBalancerRouterCommand(NetworkRouterCommand):

    def get_priority(self):
        return 65


class LoadBalancerActionCommand(
    load_balancer.LoadBalancerMixin,
    NetworkActionCommand
):
    def get_priority(self):
        return 65

    def server_enabled(self):
        return True

    def groups_allowed(self):
        return [
            Roles.admin,
            Roles.network_admin
        ]

