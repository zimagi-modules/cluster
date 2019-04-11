
class SSHTaskMixin(object):

    def _ssh_servers(self, params):
        return self.command.search_instances(
            self.manager.get_facade_index()['server'],
            queries = params.get('servers', []),
            joiner = params.get('filter', 'AND'),
            error_on_empty = False
        )

    def _ssh_exec(self, server, command, args = [], options = {}, sudo = False, ssh = None):
        if not ssh:
            ssh = server.provider.ssh()

        if sudo:
            ssh.sudo(command, *args, **options)
        else:
            ssh.exec(command, *args, **options)

