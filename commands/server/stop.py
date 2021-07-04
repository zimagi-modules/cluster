from systems.commands.index import Command


class Stop(Command('server.stop')):

    def exec(self):
        def stop_server(server):
            self.data("Stopping server", str(server))
            server.stop()

        self.run_list(self.server_instances, stop_server)
