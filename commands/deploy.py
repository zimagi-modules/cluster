from systems.commands.index import Command


class Deploy(Command('deploy')):

    def exec(self):
        env = self.create_env(self.destination,
            host = self.destination
        )
        self.data("Deploying environment to", str(env))
        self.exec_remote(env, 'db push')

        self.update_env_host(
            name = self.destination_name,
            host = self.destination
        )
