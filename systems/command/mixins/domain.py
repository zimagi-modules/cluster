from data.domain.models import Domain
from data.domain_record.models import DomainRecord
from .base import DataMixin


class DomainMixin(DataMixin):

    schema = {
        'domain': {
            'model': Domain,
            'provider': True
        },
        'domain_record': {
            'model': DomainRecord
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.facade_index['01_domain'] = self._domain
        self.facade_index['02_domain_record'] = self._domain_record
