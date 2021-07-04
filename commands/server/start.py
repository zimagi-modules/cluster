from systems.commands.index import Command


class Start(Command('server.start')):

    def exec(self):
        def start_server(server):
            self.data("Starting server", str(server))
            server.start()

        self.run_list(self.server_instances, start_server)
