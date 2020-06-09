from systems.plugins.index import BaseProvider

import os


class Provider(BaseProvider('task', 'upload')):

    def execute(self, results, params):
        mode = self.field_mode
        owner = self.field_owner
        group = self.field_group
        remote_path = self.field_remote_path
        file_path = self.get_path(self.field_file)

        if not os.path.exists(file_path):
            self.command.error("Upload task provider file {} does not exist".format(file_path))

        def exec_server(server):
            ssh = server.provider.ssh()
            ssh.upload(file_path, remote_path,
                mode = mode,
                owner = owner,
                group = group
            )

        self.command.run_list(
            self._ssh_servers(params),
            exec_server
        )
