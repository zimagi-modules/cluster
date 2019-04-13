from utility.cloud.aws import AWSServiceMixin
from .base import *


class AWSDomainProvider(AWSServiceMixin, DomainProvider):

    def provider_config(self, type = None):
        self.option(str, 'region', 'us-east-1', help = 'AWS service region')

    def add_credentials(self, config):
        self.aws_credentials(config)

    def remove_credentials(self, config):
        self.clean_aws_credentials(config)


class AWSDomainRecordProvider(AWSServiceMixin, DomainRecordProvider):

    def add_credentials(self, config):
        self.aws_credentials(config)

    def remove_credentials(self, config):
        self.clean_aws_credentials(config)


class Provider(BaseProvider):

    def register_types(self):
        super().register_types()
        self.set('domain', AWSDomainProvider)
        self.set('domain_record', AWSDomainRecordProvider)
