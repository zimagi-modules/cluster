from utility.cloud.aws import AWSServiceMixin
from .base import *


class AWSDomainProvider(AWSServiceMixin, DomainProvider):

    def provider_config(self, type = None):
        self.option(str, 'region', 'us-east-1', help = 'AWS service region')

    def initialize_terraform(self, instance, created):
        self.aws_credentials(instance.config)
        super().initialize_terraform(instance, created)

    def finalize_terraform(self, instance):
        self.aws_credentials(instance.config)
        super().finalize_terraform(instance)

    def prepare_instance(self, instance, created):
        super().prepare_instance(instance, created)
        self.clean_aws_credentials(instance.config)


class AWSDomainRecordProvider(AWSServiceMixin, DomainRecordProvider):

    def initialize_terraform(self, instance, created):
        self.aws_credentials(instance.config)
        super().initialize_terraform(instance, created)

    def finalize_terraform(self, instance):
        self.aws_credentials(instance.config)
        super().finalize_terraform(instance)

    def prepare_instance(self, instance, created):
        super().prepare_instance(instance, created)
        self.clean_aws_credentials(instance.config)


class Provider(BaseProvider):

    def register_types(self):
        super().register_types()
        self.set('domain', AWSDomainProvider)
        self.set('domain_record', AWSDomainRecordProvider)
