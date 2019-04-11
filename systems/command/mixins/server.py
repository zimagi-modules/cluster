from data.server.models import Server
from .network import NetworkMixin


class ServerMixin(NetworkMixin):

    schema = {
        'server': {
            'model': Server,
            'provider': True
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.facade_index['03_server'] = self._server
