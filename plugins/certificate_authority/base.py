from systems.plugins import base


class BaseProvider(base.BasePluginProvider):

    def __init__(self, type, name, command, domain):
        super().__init__(type, name, command)
        self.domain = domain


    def request(self):
        # Override in subclass
        pass

    def renew(self):
        # Override in subclass
        pass

    def revoke(self):
        # Override in subclass
        pass
