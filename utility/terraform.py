from .project import project_dir

import os
import pathlib
import json
import hashlib
import threading


class TerraformError(Exception):
    pass


class Terraform(object):

    thread_lock = threading.Lock()


    def __init__(self, command, id, ignore = False):
        self.lib_type = 'terraform'
        self.command = command
        self.id = id
        self.ignore = ignore


    def get_project_name(self, manifest_path, variables):
        type = os.path.basename(manifest_path).replace('.tf', '')
        return "{}-{}".format(type, self.id)


    def init(self, project, display = False):
        terraform_command = (
            'terraform',
            'init',
            '-force-copy'
        )
        with self.thread_lock:
            success = self.command.sh(
                terraform_command,
                cwd = project.base_path,
                display = display
            )
            if not success and not self.ignore:
                raise TerraformError("Terraform init failed: {}".format(" ".join(terraform_command)))


    def plan(self, manifest_path, variables, state, display_init = False):
        with project_dir(self.lib_type, self.get_project_name(manifest_path, variables)) as project:
            project.link(manifest_path, 'manifest.tf')

            self.save_variable_index(project, variables)
            if state:
                self.save_state(project, state)
            else:
                self.init(project, display_init)

            terraform_command = (
                'terraform',
                'plan',
                "-var-file={}".format(self.save_variables(project, variables))
            )
            success = self.command.sh(
                terraform_command,
                cwd = project.base_path,
                display = True
            )
            self.clean_project(project)

            if not success and not self.ignore:
                raise TerraformError("Terraform plan failed: {}".format(" ".join(terraform_command)))


    def apply(self, manifest_path, variables, state, display_init = False):
        with project_dir(self.lib_type, self.get_project_name(manifest_path, variables)) as project:
            project.link(manifest_path, 'manifest.tf')

            self.save_variable_index(project, variables)
            if state:
                self.save_state(project, state)
            else:
                self.init(project, display_init)

            terraform_command = (
                'terraform',
                'apply',
                '-auto-approve',
                "-var-file={}".format(self.save_variables(project, variables))
            )
            success = self.command.sh(
                terraform_command,
                cwd = project.base_path,
                display = True
            )
            if not success and not self.ignore:
                self.clean_project(project)
                raise TerraformError("Terraform apply failed: {}".format(" ".join(terraform_command)))

            self.command.info('')

            state = self.load_state(project)
            self.clean_project(project)
            return state


    def destroy(self, manifest_path, variables, state, display_init = False):
        with project_dir(self.lib_type, self.get_project_name(manifest_path, variables)) as project:
            project.link(manifest_path, 'manifest.tf')

            self.save_variable_index(project, variables)
            if state:
                self.save_state(project, state)
            else:
                self.init(project, display_init)

            terraform_command = [
                'terraform',
                'destroy',
                '-auto-approve',
                "-var-file={}".format(self.save_variables(project, variables))
            ]
            success = self.command.sh(
                terraform_command,
                cwd = project.base_path,
                display = True
            )
            self.clean_project(project)

            if not success and not self.ignore:
                raise TerraformError("Terraform destroy failed: {}".format(" ".join(terraform_command)))


    def save_variable_index(self, project, variables):
        index = []

        for name, value in variables.items():
            if isinstance(value, dict):
                data_type = self.parse_object(value, '  ')
            elif isinstance(value, (list, tuple)):
                data_type = 'list(string)'
            else:
                data_type = 'string'

            index.extend([
                'variable "{}" {{'.format(name),
                '  type = {}'.format(data_type),
                '}'
            ])
        return project.save("\n".join(index), 'variables.tf')

    def parse_object(self, variables, prefix):
        object = ['object({']
        inner_prefix = prefix + '  '

        for key, value in variables.items():
            if isinstance(value, dict):
                object.append("{}{} = {}".format(inner_prefix, key, self.parse_object(value, inner_prefix)))
            elif isinstance(value, (list, tuple)):
                object.append("{}{} = list(string)".format(inner_prefix, key))
            else:
                object.append("{}{} = string".format(inner_prefix, key))

        object.append("{}}})".format(prefix))
        return "\n".join(object)


    def save_variables(self, project, variables):
        return project.save(json.dumps(variables), 'variables.tfvars.json')


    def save_state(self, project, state):
        return project.save(json.dumps(state), 'terraform.tfstate')

    def load_state(self, project):
        return json.loads(project.load('terraform.tfstate'))


    def clean_project(self, project):
        project.remove('variables.tfvars.json')
        project.remove('terraform.tfstate')