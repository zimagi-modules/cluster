from systems.plugins.index import BasePlugin


class BaseProvider(BasePlugin('certificate')):

    def initialize_terraform(self, instance, created):
        if instance.domain:
            instance.private_key = instance.domain.private_key
            instance.certificate = instance.domain.certificate
            instance.chain = instance.domain.fullchain

        super().initialize_terraform(instance, created)
