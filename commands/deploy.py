from systems.commands.index import Command


class Deploy(Command('deploy')):

    def exec(self):
        host = self.save_host(
            name = self.destination_name,
            host = self.destination
        )
        self.data("Deploying environment to", str(host))
        self.exec_remote(host, 'db push')
