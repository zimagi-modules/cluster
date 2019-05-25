from django.conf import settings

from systems.command.types import server
from systems.command.mixins import db


class Command(
    db.DatabaseMixin,
    server.ServerActionCommand
):
    def parse(self):
        self.parse_server_search(False)
        self.parse_variable('destination', '--dest', str,
            'environment runtime host destination',
            value_label = 'HOST'
        )
        self.parse_variable('destination_name', '--dest-name', str,
            'destination environment runtime host name',
            value_label = 'NAME'
        )

    def exec(self):
        destination = self.options.get('destination', None)
        destination_name = self.options.get('destination_name', settings.DEFAULT_HOST_NAME)

        def deploy_env(env):
            self.data("Deploying environment to", str(env))
            self.exec_remote(env, 'db push')

        self.run_list(
            self._update_environments(self.server_instances),
            deploy_env
        )
        if destination:
            self.update_env_host(
                name = destination_name,
                host = destination
            )

    def _update_environments(self, servers):
        env_name = self._environment.get_env()
        environments = []
        for index, server in enumerate(servers):
            environments.append(self.create_env("{}-{}".format(env_name, index),
                host = server.ip
            ))
        return environments
