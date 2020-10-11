from systems.plugins.index import BasePlugin


class BaseProvider(BasePlugin('database')):

    def prepare_instance(self, instance, created):
        self.update_domain_reference(instance)

    def finalize_terraform(self, instance):
        self.remove_domain_reference(instance)
        super().finalize_terraform(instance)


    def update_domain_reference(self, instance):
        if instance.domain and instance.host:
            domain_target = "{}.{}".format(
                instance.name,
                instance.domain.name
            )
            domain_name = "{}-{}".format(domain_target, instance.host)

            record = self.command._domain_record.retrieve(
                domain_name,
                domain = instance.domain
            )
            if not record:
                provider = self.command.get_provider(
                    self.command._domain_record.meta.provider_name,
                    instance.domain.provider_type
                )
                record = provider.create(domain_name, {
                    'domain': instance.domain,
                    'target': domain_target,
                    'type': 'CNAME',
                    'values': [ instance.host ]
                })
            else:
                record.initialize(self.command)
                record.provider.update()

    def remove_domain_reference(self, instance):
        if instance.domain and instance.host:
            domain_target = "{}.{}".format(
                instance.name,
                instance.domain.name
            )
            domain_name = "{}-{}".format(domain_target, instance.host)

            record = self.command._domain_record.retrieve(
                domain_name,
                domain = instance.domain
            )
            if record:
                record.initialize(self.command)
                record.provider.delete()
