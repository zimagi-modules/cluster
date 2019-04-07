from systems.plugins import meta, terraform
from utility.data import ensure_list


class LoadBalancerProvider(terraform.TerraformPluginProvider):

    def terraform_type(self):
        return 'load_balancer'

    @property
    def facade(self):
        return self.command._load_balancer

    def prepare_instance(self, instance, created):
        super().prepare_instance(instance, created)
        self.update_domain_reference(instance)

    def finalize_terraform(self, instance):
        self.remove_domain_reference(instance)
        super().finalize_terraform(instance)


    def update_domain_reference(self, instance):
        if instance.domain:
            dns_name = instance.variables['lb_dns_name']
            domain_target = "{}.{}".format(
                instance.name,
                instance.domain.name
            )
            record = self.command._domain_record.retrieve(
                domain_target,
                domain = instance.domain
            )
            if not record:
                provider = self.command.get_provider(
                    self.command._domain_record.meta.provider_name,
                    instance.domain.provider_type
                )
                record = provider.create(domain_target, {
                    'domain': instance.domain,
                    'target': domain_target,
                    'type': 'CNAME',
                    'values': [
                        dns_name
                    ]
                })
            else:
                if dns_name not in record.values:
                    record.values.append(dns_name)
                    record.provider.update()

    def remove_domain_reference(self, instance):
        if instance.domain:
            dns_name = instance.variables['lb_dns_name']
            domain_target = "{}.{}".format(
                instance.name,
                instance.domain.name
            )
            record = self.command._domain_record.retrieve(
                domain_target,
                domain = instance.domain
            )
            if record:
                if dns_name in record.values:
                    record.values.remove(dns_name)
                    if record.values:
                        record.provider.update()
                    else:
                        record.provider.delete()


class LoadBalancerListenerProvider(terraform.TerraformPluginProvider):

    def terraform_type(self):
        return 'load_balancer_listener'

    @property
    def facade(self):
        return self.command._load_balancer_listener

    def initialize_terraform(self, instance, created):
        super().initialize_terraform(instance, created)
        instance.healthy_status = ensure_list(instance.healthy_status)


class BaseProvider(meta.MetaPluginProvider):

    def register_types(self):
        self.set('load_balancer', LoadBalancerProvider)
        self.set('load_balancer_listener', LoadBalancerListenerProvider)
