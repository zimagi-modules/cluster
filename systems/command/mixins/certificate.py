from data.certificate.models import Certificate
from .base import DataMixin


class CertificateMixin(DataMixin):

    schema = {
        'certificate': {
            'model': Certificate,
            'provider': True
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.facade_index['02_certificate'] = self._certificate
