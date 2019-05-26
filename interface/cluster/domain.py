from systems.command.base import command_set
from systems.command.factory import resource, router
from systems.command.types import domain


class Command(domain.DomainRouterCommand):

    def get_subcommands(self):
        domain_record_name = 'domain_record'

        return command_set(
            resource.ResourceCommandSet(
                domain.DomainActionCommand, self.name,
                provider_name = self.name,
                provider_subtype = self.name
            ),
            ('record', router.Router(
                domain.DomainRouterCommand,
                resource.ResourceCommandSet(
                    domain.DomainActionCommand, domain_record_name,
                    provider_name = self.name,
                    provider_subtype = domain_record_name
                )
            ))
        )
