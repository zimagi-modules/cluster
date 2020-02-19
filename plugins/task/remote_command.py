from .base import BaseProvider
from .mixins import cli, ssh


class Provider(
    cli.CLITaskMixin,
    ssh.SSHTaskMixin,
    BaseProvider
):
    def get_fields(self):
        return {
            'command': '<required>',
            'env': {},
            'servers': '<required>,...',
            'filter': 'AND',
            'sudo': False,
            'lock': False,
            'options': {}
        }

    def execute(self, results, params):
        if 'command' in self.config:
            command = self.config['command']
        else:
            self.command.error("Remote command task provider must have a 'command' property specified")

        env = self._env_vars(params)
        sudo = self.config.get('sudo', False)
        lock = self.config.get('lock', False)
        options = self._merge_options(self.config.get('options', {}), params, lock)

        command = self._interpolate(command, options)
        if sudo:
            command = 'sudo ' + command[0]
        else:
            command = command[0]

        def exec_server(server):
            self._ssh_exec(server, command,
                env = env,
                sudo = sudo
            )

        self.command.run_list(
            self._ssh_servers(params),
            exec_server
        )
