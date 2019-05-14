from data.server.models import Server
from data.server_volume.models import ServerVolume
from .network import NetworkMixin


class ServerMixin(NetworkMixin):

    schema = {
        'server': {
            'model': Server,
            'provider': True
        },
        'server_volume': {
            'model': ServerVolume,
            'provider': True
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.facade_index['03_server'] = self._server
        self.facade_index['04_server_volume'] = self._server_volume
