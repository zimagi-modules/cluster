from django.conf import settings

from systems.command.types import server
from systems.command.mixins import db


class Command(
    db.DatabaseMixin,
    server.ServerActionCommand
):
    def parse(self):
        self.parse_server_search(False)
        self.parse_environment_host('--host')

    def exec(self):
        host = self.environment_host

        def deploy_env(env):
            self.data("Deploying environment to", str(env))
            self.exec_remote(env, 'db push')

        self.run_list(
            self._update_environments(self.server_instances),
            deploy_env
        )
        if host:
            self.environment.provider.update({
                'host': host
            })

    def _update_environments(self, servers):
        curr_env = self._environment.get_env()
        environments = []
        for index, server in enumerate(servers):
            environments.append(self._environment.create("{}-{}".format(curr_env, index),
                host = server.ip
            ))
        return environments
