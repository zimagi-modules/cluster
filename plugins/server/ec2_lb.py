from plugins.server import ec2


class Provider(ec2.Provider):

    def initialize_terraform(self, instance, created):
        super().initialize_terraform(instance, created)

        relations = self.command.get_relations(instance.facade)
        instance.config['listeners'] = self.get_instance_values(
            relations['load_balancer_listeners'],
            instance.load_balancer_listeners,
            self.command._load_balancer_listener
        )
