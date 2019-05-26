import os
import boto3


class AWSServiceMixin(object):

    def aws_credentials(self, config = {}):
        try:
            config['access_key'] = self.command.get_config('aws_access_key', required = True).strip()
            os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']

            config['secret_key'] = self.command.get_config('aws_secret_key', required = True).strip()
            os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']

        except Exception:
            self.command.error("To use AWS provider you must have 'aws_access_key' and 'aws_secret_key' environment configurations; see: config save")

        return config

    def clean_aws_credentials(self, config):
        config.pop('access_key', None)
        os.environ.pop('AWS_ACCESS_KEY_ID', None)

        config.pop('secret_key', None)
        os.environ.pop('AWS_SECRET_ACCESS_KEY', None)


    def _init_session(self):
        if not getattr(self, 'session', None):
            config = self.aws_credentials()
            self.session = boto3.Session(
                aws_access_key_id = config['access_key'],
                aws_secret_access_key = config['secret_key']
            )

    def ec2(self, network):
        self._init_session()
        return self.session.client('ec2',
            region_name = network.config['region']
        )

    def efs(self, network):
        self._init_session()
        return self.session.client('efs',
            region_name = network.config['region']
        )


    def get_subnets(self, names, network):
        subnet_ids = []

        if names:
            subnets = self.command.get_instances(self.command._subnet, names = names)
            for subnet in subnets:
                subnet_ids.append(subnet.variables['subnet_id'])
        else:
            for subnet in network.subnet_relation.all():
                subnet_ids.append(subnet.variables['subnet_id'])

        return subnet_ids

    def get_nat_route_tables(self, names, subnets):
        route_table_ids = []

        if names:
            subnets = self.command.get_instances(self.command._subnet, names = names)
            for subnet in subnets:
                route_table_ids.append(subnet.variables['nat_route_table_id'])
        else:
            for subnet in subnets.all():
                route_table_ids.append(subnet.variables['nat_route_table_id'])

        return route_table_ids

    def get_security_groups(self, names, firewalls):
        sgroups = []

        if names:
            firewalls = self.command.get_instances(self.command._firewall, names = names)
            for firewall in firewalls:
                sgroups.append(firewall.variables['security_group_id'])
        else:
            for firewall in firewalls.all():
                sgroups.append(firewall.variables['security_group_id'])

        return sgroups
