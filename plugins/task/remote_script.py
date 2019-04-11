from utility.data import ensure_list
from .base import BaseProvider
from .mixins import cli, ssh

import os


class Provider(
    cli.CLITaskMixin,
    ssh.SSHTaskMixin,
    BaseProvider
):
    def execute(self, results, params):
        def exec_server(server):
            if 'script' in self.config:
                script_path = self.get_path(self.config['script'])
            else:
                self.command.error("Remote script task provider must have a 'script' property specified that links to an executable file")

            if not os.path.exists(script_path):
                self.command.error("Remote script task provider file {} does not exist".format(script_path))

            script_base, script_ext = os.path.splitext(script_path)
            temp_path = "/tmp/{}{}".format(self.generate_name(24), script_ext)

            sudo = self.config.get('sudo', False)
            lock = self.config.get('lock', False)
            options = self._merge_options(self.config.get('options', {}), params, lock)
            args = ensure_list(self.config.get('args', []))

            ssh = server.provider.ssh()
            ssh.upload(script_path, temp_path, mode = 0o755)
            try:
                self._ssh_exec(server, temp_path,
                    self._interpolate(args, options),
                    sudo = sudo,
                    ssh = ssh
                )
            finally:
                ssh.sudo('rm -f', temp_path)

        self.command.run_list(
            self._ssh_servers(params),
            exec_server
        )
