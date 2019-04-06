from data.load_balancer.models import LoadBalancer
from data.load_balancer_listener.models import LoadBalancerListener
from .base import DataMixin


class LoadBalancerMixin(DataMixin):

    schema = {
        'load_balancer': {
            'model': LoadBalancer,
            'provider': True
        },
        'load_balancer_listener': {
            'model': LoadBalancerListener
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.facade_index['02_load_balancer'] = self._load_balancer
        self.facade_index['03_load_balancer_listener'] = self._load_balancer_listener
