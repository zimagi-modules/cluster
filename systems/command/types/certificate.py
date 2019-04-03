from settings.roles import Roles
from .router import RouterCommand
from .action import ActionCommand
from systems.command.mixins import certificate


class CertificateRouterCommand(RouterCommand):

    def get_priority(self):
        return 65


class CertificateActionCommand(
    certificate.CertificateMixin,
    ActionCommand
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

