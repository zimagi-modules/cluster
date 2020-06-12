from systems.commands.index import Command


class Deploy(Command('deploy')):

    def exec(self):

        def deploy_env(env):
            self.data("Deploying environment to", str(env))
            self.exec_remote(env, 'db push')

        self.run_list(
            self._update_environments(self.server_instances),
            deploy_env
        )
        if self.destination:
            self.update_env_host(
                name = self.destination_name,
                host = self.destination
            )

    def _update_environments(self, servers):
        env_name = self._environment.get_env()
        environments = []
        for index, server in enumerate(servers):
            environments.append(self.create_env("{}-{}".format(env_name, index),
                host = server.ip
            ))
        return environments
