from io import StringIO

from django.conf import settings
from django.core.management.base import CommandError

from systems.plugins import terraform
from utility import ssh as sshlib

import threading
import time
import copy


class SSHAccessError(CommandError):
    pass


class BaseProvider(terraform.TerraformPluginProvider):

    def terraform_type(self):
        return 'server'

    @property
    def facade(self):
        return self.command._server

    def prepare_instance(self, instance, created):
        if not self.check_ssh(instance = instance):
            self.command.error("Can not establish SSH connection to: {}".format(instance), error_cls = SSHAccessError)


    def rotate_key(self):
        instance = self.check_instance('server rotate key')
        (private_key, public_key) = sshlib.SSH.create_keypair()

        ssh = self.ssh()
        ssh.exec('mkdir -p "$HOME/.ssh"')
        ssh.exec('chmod 700 "$HOME/.ssh"')
        ssh.exec('echo "{}" > "$HOME/.ssh/authorized_keys"'.format(public_key))
        ssh.exec('chmod 600 "$HOME/.ssh/authorized_keys"')

        instance.private_key = private_key

    def rotate_password(self):
        instance = self.check_instance('server rotate password')
        password = sshlib.SSH.create_password()
        module = self.command.get_instance(
            self.command._module,
            self.manager.module_name(__file__)
        )

        module.provider.exec_task(
            'password',
            {
                "user": instance.user,
                "password": password
            }
        )
        instance.password = password


    def ssh(self, timeout = 10):
        instance = self.check_instance('server ssh')
        return self.command.ssh(
            instance.ip, instance.user,
            password = instance.password,
            key = instance.private_key,
            timeout = timeout,
            port = instance.ssh_port
        )

    def check_ssh(self, tries = 10, interval = 2, timeout = 10, silent = False, instance = None):
        if not self.instance and not instance:
            self.command.error("Checking SSH requires a valid server instance given to provider on initialization")
        if not instance:
            instance = self.instance

        while True:
            if not tries:
                break
            try:
                if not silent:
                    self.command.info("Checking {}@{}:{} SSH connection".format(instance.user, instance.ip, instance.ssh_port))

                sshlib.SSH(instance.ip, instance.user, instance.password,
                    key = instance.private_key,
                    timeout = timeout,
                    port = instance.ssh_port
                )
                return True

            except Exception as e:
                time.sleep(interval)
                tries -= 1

        return False

    def ping(self):
        return self.check_ssh(
            tries = 1,
            timeout = 1,
            silent = True
        )
