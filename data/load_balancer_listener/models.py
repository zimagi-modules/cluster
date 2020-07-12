from systems.models.base import model_index
from systems.models.index import Model, ModelFacade
from utility.data import ensure_list


class LoadBalancerListener(Model('load_balancer_listener')):

    @property
    def servers(self):
        server_facade = model_index().get_facade_index()['server']
        return list(server_facade.filter(
            groups__name__in = ensure_list(self.server_groups),
            subnet__in = list(self.load_balancer.subnets.all())
        ))
