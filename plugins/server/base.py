from io import StringIO

from django.conf import settings
from django.core.management.base import CommandError

from systems.plugins.index import BasePlugin
from utility import ssh as sshlib

import threading
import time
import copy


class SSHAccessError(CommandError):
    pass


class BaseProvider(BasePlugin('server')):

    def prepare_instance(self, instance, created):
        if not self.check_ssh(instance = instance):
            self.command.error("Can not establish SSH connection to: {}".format(instance), error_cls = SSHAccessError)
        self.update_domain_reference(instance)

    def finalize_terraform(self, instance):
        self.remove_domain_reference(instance)
        super().finalize_terraform(instance)


    def update_domain_reference(self, instance):
        if instance.domain and instance.public_ip:
            domain_target = "{}.{}".format(
                instance.domain_name if instance.domain_name else instance.name,
                instance.domain.name
            )
            domain_name = "{}-{}".format(domain_target, instance.public_ip)

            record = self.command._domain_record.retrieve(
                domain_name,
                domain = instance.domain
            )
            if not record:
                provider = self.command.get_provider(
                    self.command._domain_record.meta.provider_name,
                    instance.domain.provider_type
                )
                record = provider.create(domain_name, {
                    'domain': instance.domain,
                    'target': domain_target,
                    'type': 'A',
                    'values': [ instance.public_ip ]
                })
            else:
                record.initialize(self.command)
                record.provider.update()

    def remove_domain_reference(self, instance):
        if instance.domain and instance.public_ip:
            domain_target = "{}.{}".format(
                instance.domain_name if instance.domain_name else instance.name,
                instance.domain.name
            )
            domain_name = "{}-{}".format(domain_target, instance.public_ip)

            record = self.command._domain_record.retrieve(
                domain_name,
                domain = instance.domain
            )
            if record:
                record.initialize(self.command)
                record.provider.delete()


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
            self.manager.index.get_module_name(__file__)
        )

        module.provider.exec_task(
            'password',
            {
                "servers": "id={}".format(instance.id),
                "user": instance.user,
                "password": password
            }
        )
        instance.password = password


    def ssh(self, timeout = 10, env = None):
        if not env:
            env = {}

        instance = self.check_instance('server ssh')
        return self.command.ssh(
            instance.ip, instance.user,
            password = instance.password,
            key = instance.private_key,
            timeout = timeout,
            port = instance.ssh_port,
            env = env
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


    def start(self):
        # Override in subclass
        pass

    def stop(self):
        # Override in subclass
        pass
