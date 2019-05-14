from systems.plugins import terraform


class BaseProvider(terraform.TerraformPluginProvider):

    def terraform_type(self):
        return 'server_volume'

    @property
    def facade(self):
        return self.command._server_volume

    def prepare_instance(self, instance, created):
        super().prepare_instance(instance, created)
        self.mount_volume(instance)


    def mount_volume(self, instance):
        module = self.command.get_instance(
            self.command._module,
            self.manager.module_name(__file__)
        )
        module.provider.exec_task(
            'mount',
            {
                "servers": "id={}".format(instance.id),
                "mounts": [
                    {
                        'path': instance.name,
                        'source': instance.source,
                        'type': instance.type,
                        'options': ",".join(instance.options),
                        'owner': instance.owner,
                        'group': instance.group,
                        'mode': instance.mode
                    }
                ]
            }
        )
