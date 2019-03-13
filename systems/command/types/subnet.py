from settings.roles import Roles
from .network import NetworkRouterCommand, NetworkActionCommand


class SubnetRouterCommand(NetworkRouterCommand):

    def get_priority(self):
        return 55


class SubnetActionCommand(NetworkActionCommand):

    def get_priority(self):
        return 55

