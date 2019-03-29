from data.network.models import Network
from data.subnet.models import Subnet
from data.firewall.models import Firewall
from data.firewall_rule.models import FirewallRule
from .base import DataMixin


class NetworkMixin(DataMixin):

    schema = {
        'network': {
            'model': Network,
            'provider': True
        },
        'subnet': {
            'model': Subnet
        },
        'firewall': {
            'model': Firewall
        },
        'firewall_rule': {
            'model': FirewallRule
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.facade_index['01_network'] = self._network
        self.facade_index['02_subnet'] = self._subnet
        self.facade_index['02_firewall'] = self._firewall
        self.facade_index['03_firewall_rule'] = self._firewall_rule
