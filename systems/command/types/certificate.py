from settings.roles import Roles
from .network import NetworkRouterCommand, NetworkActionCommand
from systems.command.mixins import certificate, domain


class CertificateRouterCommand(NetworkRouterCommand):

    def get_priority(self):
        return 65


class CertificateActionCommand(
    domain.DomainMixin,
    certificate.CertificateMixin,
    NetworkActionCommand
):
    def get_priority(self):
        return 65

    def server_enabled(self):
        return True

    def groups_allowed(self):
        return [
            Roles.admin,
            Roles.security_admin
        ]

