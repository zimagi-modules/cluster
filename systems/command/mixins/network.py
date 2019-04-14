from data.network.models import Network
from data.network_peering.models import NetworkPeering
from data.network_peering_relation.models import NetworkPeeringRelation
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
        'network_peering': {
            'model': NetworkPeering,
            'provider': True
        },
        'network_relation': {
            'model': NetworkPeeringRelation
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
        self.facade_index['02_network_peering'] = self._network_peering
        self.facade_index['03_network_relation'] = self._network_relation
        self.facade_index['02_subnet'] = self._subnet
        self.facade_index['02_firewall'] = self._firewall
        self.facade_index['03_firewall_rule'] = self._firewall_rule
