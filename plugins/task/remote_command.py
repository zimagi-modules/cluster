from systems.plugins.index import BaseProvider


class Provider(BaseProvider('task', 'remote_command')):

    def execute(self, results, params):
        env = self._env_vars(params)
        options = self._merge_options(self.field_options, params, self.field_lock)

        command = self._interpolate(self.field_command, options)
        sudo = self.field_sudo
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
