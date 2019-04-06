from systems.plugins import meta, terraform


class LoadBalancerProvider(terraform.TerraformPluginProvider):

    def terraform_type(self):
        return 'load_balancer'

    @property
    def facade(self):
        return self.command._load_balancer


class LoadBalancerListenerProvider(terraform.TerraformPluginProvider):

    def terraform_type(self):
        return 'load_balancer_listener'

    @property
    def facade(self):
        return self.command._load_balancer_listener


class BaseProvider(meta.MetaPluginProvider):

    def register_types(self):
        self.set('load_balancer', LoadBalancerProvider)
        self.set('load_balancer_listener', LoadBalancerListenerProvider)
