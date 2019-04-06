from systems.command.base import command_list
from systems.command.factory import resource, router
from systems.command.types import load_balancer


class Command(load_balancer.LoadBalancerRouterCommand):

    def get_subcommands(self):
        name = 'load_balancer'
        listener_name = 'load_balancer_listener'

        return command_list(
            resource.ResourceCommandSet(
                load_balancer.LoadBalancerActionCommand, name,
                provider_name = name,
                provider_subtype = name
            ),
            ('listener', router.Router(
                load_balancer.LoadBalancerRouterCommand,
                resource.ResourceCommandSet(
                    load_balancer.LoadBalancerActionCommand, listener_name,
                    provider_name = name,
                    provider_subtype = listener_name
                )
            ))
        )
