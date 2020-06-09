from systems.plugins.index import BaseProvider


class Provider(BaseProvider('server', 'ec2_lb')):

    def initialize_terraform(self, instance, created):
        super().initialize_terraform(instance, created)

        relations = self.command.get_relations(instance.facade)
        instance.config['listeners'] = self.get_instance_values(
            relations['load_balancer_listeners'],
            instance.load_balancer_listeners,
            self.command._load_balancer_listener
        )
