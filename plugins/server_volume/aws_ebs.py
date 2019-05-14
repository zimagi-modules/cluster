from utility.cloud.aws import AWSServiceMixin
from .base import BaseProvider


class Provider(AWSServiceMixin, BaseProvider):

    def provider_config(self, type = None):
        self.option(bool, 'ebs_encrypted', False, help = 'AWS EBS encrypted volume?', config_name = 'aws_ec2_ebs_encrypted')
        self.option(str, 'ebs_type', 'gp2', help = 'AWS data drive EBS type', config_name = 'aws_ec2_ebs_type')
        self.option(int, 'ebs_size', 10, help = 'AWS data drive EBS volume size (GB)', config_name = 'aws_ec2_ebs_size')
        self.option(int, 'ebs_iops', None, help = 'AWS data drive EBS provisioned IOPS', config_name = 'aws_ec2_ebs_size')

    def add_credentials(self, config):
        self.aws_credentials(config)

    def remove_credentials(self, config):
        self.clean_aws_credentials(config)
