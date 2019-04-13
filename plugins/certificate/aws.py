from utility.cloud.aws import AWSServiceMixin
from .base import BaseProvider


class Provider(AWSServiceMixin, BaseProvider):

    def add_credentials(self, config):
        self.aws_credentials(config)

    def remove_credentials(self, config):
        self.clean_aws_credentials(config)
