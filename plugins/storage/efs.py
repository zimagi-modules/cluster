from systems.plugins.index import BaseProvider


class MountProvider(BaseProvider('storage.mount', 'efs')):

    def initialize_terraform(self, instance, created):
        relations = self.command.get_relations(instance.facade)
        super().initialize_terraform(instance, created)
        instance.config['security_groups'] = self.get_security_groups(relations['firewalls'], instance.firewalls)

    def prepare_instance(self, instance, created):
        instance.remote_path = '/'
        instance.remote_host = instance.variables['mount_ip']
        super().prepare_instance(instance, created)
