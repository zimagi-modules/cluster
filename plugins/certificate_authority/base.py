from systems.plugins.index import BasePlugin


class BaseProvider(BasePlugin('certificate_authority')):

    def __init__(self, type, name, command, domain):
        super().__init__(type, name, command)
        self.domain = domain
