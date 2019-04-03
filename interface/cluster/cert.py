from systems.command.factory import resource
from systems.command.types import certificate


class Command(domain.DomainRouterCommand):

    def get_subcommands(self):
        name = 'certificate'
        return resource.ResourceCommandSet(
            certificate.CertificateActionCommand, name,
            provider_name = name
        )
