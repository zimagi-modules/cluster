from systems.commands.index import Command


class Rotate(Command('server.rotate')):

    def exec(self):
        def rotate_server(server):
            self.data("Rotating SSH keypair for", str(server))
            server.provider.rotate_password()
            server.provider.rotate_key()
            server.save()

        self.run_list(self.server_instances, rotate_server)
