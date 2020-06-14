from systems.plugins.index import BasePlugin

import itertools


class NetworkPeeringBaseProvider(BasePlugin('network_peering.network_peering')):

    def store_related(self, instance, created, test):
        relation_facade = self.command._network_peering_relation
        relations = self.command.get_relations(instance.facade)

        if relations['networks']:
            networks = self.command.get_instances(self.command._network, names = relations['networks'])

            def save_relation(relation):
                network1, network2 = sorted(relation, key = lambda x: (x.provider_type, x.name))

                relation_name = "{}:{}".format(network1.name, network2.name)
                relation_fields = {
                    'network_peering': instance,
                    'network1': network1,
                    'network2': network2
                }
                relation_instance = self.command.get_instance(relation_facade, relation_name, required = False)
                if not relation_instance:
                    self.command.get_provider(
                        relation_facade.meta.provider_name,
                        instance.provider_type
                    ).create(relation_name, relation_fields)
                else:
                    relation_instance.provider.update(relation_fields)

            self.command.run_list(itertools.combinations(networks, 2), save_relation)


    def finalize_instance(self, instance):

        def remove_relation(relation):
            relation.initialize(self.command)
            relation.network1.initialize(self.command)
            relation.network2.initialize(self.command)
            relation.provider.delete()

        self.command.run_list(
            self.command._network_peering_relation.query(network_peering_id = instance.id),
            remove_relation
        )


class NetworkRelationBaseProvider(BasePlugin('network_peering.network_relation')):

    def get_terraform_name(self, instance):
        return "{}_{}".format(
            instance.network1.provider_type,
            instance.network2.provider_type
        )


    def initialize_terraform(self, instance, created):
        instance.terraform_name = self.get_terraform_name(instance)
        instance.network1.provider.add_credentials(instance.config)
        instance.network2.provider.add_credentials(instance.config)
        super().initialize_terraform(instance, created)

    def prepare_instance(self, instance, created):
        super().prepare_instance(instance, created)
        instance.network1.provider.remove_credentials(instance.config)
        instance.network2.provider.remove_credentials(instance.config)

    def finalize_instance(self, instance):
        instance.terraform_name = self.get_terraform_name(instance)
        instance.network1.provider.add_credentials(instance.config)
        instance.network2.provider.add_credentials(instance.config)
        super().finalize_instance(instance)
