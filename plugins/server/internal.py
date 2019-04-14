from .base import BaseProvider


class Provider(BaseProvider):

    def provider_config(self, type = None):
        self.requirement(str, 'public_ip', help = 'Public IP of server')
        self.requirement(str, 'private_ip', help = 'Private IP of server')
        self.requirement(str, 'password', help = 'Password of server user')

        self.option(str, 'user', 'admin', help = 'Server SSH user', config_name = 'internal_user')
        self.option(str, 'data_device', '/dev/sda4', help = 'Server data drive device', config_name = 'internal_data_device')
