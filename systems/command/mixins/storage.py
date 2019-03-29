from data.storage.models import Storage
from data.storage_mount.models import StorageMount
from .network import NetworkMixin


class StorageMixin(NetworkMixin):

    schema = {
        'storage': {
            'model': Storage,
            'provider': True
        },
        'mount': {
            'model': StorageMount
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.facade_index['02_storage'] = self._storage
        self.facade_index['03_mount'] = self._mount
