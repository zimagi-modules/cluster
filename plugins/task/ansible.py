from .base import BaseProvider
from .mixins import cli, ssh
from utility.runtime import Runtime
from utility.temp import temp_dir
from utility.data import clean_dict, ensure_list

import os
import re
import json


class AnsibleInventory(object):

    def __init__(self, provider, servers, temp):
        self.temp = temp

        self.provider = provider
        self.servers = servers
        self.hosts = []
        self.groups = {}

        self.generate_hosts()
        self.group_servers()


    def get_server_id(self, server):
        return "{}-{}".format(server.name.replace('_', '-'), server.ip)


    def generate_hosts(self):
        self.hosts = []

        for server in self.servers:
            host = clean_dict({
                'server': server,
                'ansible_host': server.ip,
                'ansible_port': server.ssh_port,
                'ansible_user': server.user,
                'ansible_ssh_pass': server.password,
                'ansible_become': 'yes',
                'ansible_become_user': 'root',
                'ansible_become_pass': server.password,
                'ansible_python_interpreter': '/usr/bin/python3'
            })
            if server.private_key:
                host['ansible_ssh_private_key_file'] = self.temp.save(
                    server.private_key,
                    directory = 'keys'
                )
            self.hosts.append(host)

    def group_servers(self):
        self.groups = {}

        for server in self.servers:
            for group in server.groups.all():
                if group.name not in self.groups:
                    self.groups[group.name] = {
                        'children': [],
                        'servers': []
                    }
                self.groups[group.name]['servers'].append(self.get_server_id(server))

                while group.parent:
                    if group.parent.name not in self.groups:
                        self.groups[group.parent.name] = {
                            'children': [],
                            'servers': []
                        }
                    if group.name not in self.groups[group.parent.name]['children']:
                        self.groups[group.parent.name]['children'].append(group.name)

                    group = group.parent

    def render(self):
        data = [ '[all]' ]
        for host in self.hosts:
            record = [ self.get_server_id(host.get('server')) ]

            for key, value in host.items():
                if key != 'server':
                    record.append("{}={}".format(key, value))

            data.append(" ".join(record))
        data.append('')

        for name, info in self.groups.items():
            if len(info['children']):
                data.append("[{}:children]".format(name))
                for child in info['children']:
                    data.append(child)
                data.append('')

            if len(info['servers']):
                data.append("[{}]".format(name))
                for server in info['servers']:
                    data.append(server)
                data.append('')

        return "\n".join(data)


class Provider(
    cli.CLITaskMixin,
    ssh.SSHTaskMixin,
    BaseProvider
):
    def execute(self, results, params):
        with temp_dir() as temp:
            lock = self.config.get('lock', False)
            ansible_config = self.merge_config(self.config.get('config', None),
                '[defaults]',
                'host_key_checking = False',
                'deprecation_warnings = False',
                'gathering = smart'
            )
            inventory = AnsibleInventory(self, self._ssh_servers(params), temp)

            if 'group_vars' in self.config:
                temp.link(self.get_path(self.config['group_vars']),
                    name = 'group_vars'
                )

            ansible_cmd = [
                'ansible-playbook',
                '-i', temp.save(inventory.render())
            ]
            #if Runtime.debug():
            #    ansible_cmd.append('-vvv')

            if 'playbooks' in self.config:
                command = ansible_cmd + ensure_list(self.config['playbooks'])

                if lock:
                    params = {}
                else:
                    params.pop('servers', None)
                    params.pop('filter', None)

                if 'variables' in self.config:
                    for key, value in self.config['variables'].items():
                        if key not in params:
                            params[key] = value

                if params:
                    command.extend([
                        "--extra-vars",
                        "@{}".format(temp.save(json.dumps(params), extension = 'json'))
                    ])
            else:
                self.command.error("Ansible task requires 'playbooks' list configuration")

            success = self.command.sh(
                command,
                env = {
                    "ANSIBLE_CONFIG": temp.save(ansible_config, extension = 'cfg')
                },
                cwd = self.get_module_path(),
                display = True
            )
            if not success:
                self.command.error("Ansible task failed: {}".format(" ".join(command)))


    def merge_config(self, config_file_name, *core_config):
        if not config_file_name:
            return "\n".join(core_config)

        config_contents = self.module.load_file(config_file_name)

        if not config_contents:
            self.command.error("Could not load configuration from: {}".format(config_file_name))

        config = []
        sections = {}
        curr_section = '[defaults]'

        for line in config_contents.split("\n") + list(core_config):
            line = line.strip()

            if line:
                match = re.search(r'^\[\s*([^\]]+)\s*\]$', line)
                if match:
                    curr_section = match.group(1)

                    if curr_section not in sections:
                        sections[curr_section] = []
                else:
                    if line[0] != '#':
                        sections[curr_section].append(line)

        for section, lines in sections.items():
            config.append("[{}]".format(section))
            config.extend(lines)
            config.append('')

        return "\n".join(config)
