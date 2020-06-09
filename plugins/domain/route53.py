from systems.plugins.index import BaseProvider


class DomainProvider(BaseProvider('domain.domain', 'route53')):

    def add_credentials(self, config):
        self.aws_credentials(config)

    def remove_credentials(self, config):
        self.clean_aws_credentials(config)


class DomainRecordProvider(BaseProvider('domain.domain_record', 'route53')):

    def add_credentials(self, config):
        self.aws_credentials(config)

    def remove_credentials(self, config):
        self.clean_aws_credentials(config)
