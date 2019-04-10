
class SSHTaskMixin(object):

    def _ssh_exec(self, server, command, args = [], options = {}, sudo = False, ssh = None):
        if not ssh:
            ssh = server.provider.ssh()

        if sudo:
            ssh.sudo(command, *args, **options)
        else:
            ssh.exec(command, *args, **options)

