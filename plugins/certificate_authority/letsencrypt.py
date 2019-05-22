from django.conf import settings

from .base import BaseProvider
from utility.temp import temp_dir

import datetime
import os
import pathlib


class Provider(BaseProvider):

    @property
    def root_directory(self):
        certbot_config_dir = os.path.join(settings.LIB_DIR, 'certbot', self.domain.name)
        pathlib.Path(certbot_config_dir).mkdir(mode = 0o700, parents = True, exist_ok = True)
        return certbot_config_dir

    @property
    def renewal_directory(self):
        return "{}/renewal/{}".format(
            self.root_directory,
            self.domain.name
        )

    @property
    def live_directory(self):
        return "{}/live/{}".format(
            self.root_directory,
            self.domain.name
        )


    def request(self):
        with temp_dir() as temp:
            self.command.info('Requesting certbot certificate for domain')
            self.certbot(temp, 'certonly',
                '--cert-name', self.domain.name,
                '-d', "*.{}".format(self.domain.name),
                '-m', self.domain.email
            )

    def renew(self):
        with temp_dir() as temp:
            self.command.info('Renewing certbot certificate for domain')
            self.certbot(temp, 'certonly',
                '--force-renewal',
                '--cert-name', self.domain.name,
                '-d', "*.{}".format(self.domain.name),
                '-m', self.domain.email
            )

    def revoke(self):
        with temp_dir() as temp:
            self.command.info('Revoking certbot certificate for domain')
            self.certbot(temp, 'revoke',
                '--cert-path', "{}/fullchain.pem".format(self.live_directory),
                '-d', "*.{}".format(self.domain.name),
                '-m', self.domain.email
            )
            self.domain.private_key = None
            self.domain.certificate = None
            self.domain.fullchain = None
            self.domain.chain = None
            self.domain.certificate_updated = None


    def init_temp_dir(self, temp):
        cert_dir = self.live_directory

        temp.mkdir('work')
        temp.mkdir('logs')

        if self.domain.private_key:
            temp.save(self.domain.private_key, 'privkey.pem',
                directory = cert_dir
            )
        if self.domain.certificate:
            temp.save(self.domain.certificate, 'cert.pem',
                directory = cert_dir
            )
        if self.domain.fullchain:
            temp.save(self.domain.fullchain, 'fullchain.pem',
                directory = cert_dir
            )
        if self.domain.chain:
            temp.save(self.domain.chain, 'chain.pem',
                directory = cert_dir
            )

    def save_certificates(self, temp):
        cert_dir = self.live_directory

        self.domain.private_key = temp.load('privkey.pem',
            directory = cert_dir
        )
        self.domain.certificate = temp.load('cert.pem',
            directory = cert_dir
        )
        self.domain.fullchain = temp.load('fullchain.pem',
            directory = cert_dir
        )
        self.domain.chain = temp.load('chain.pem',
            directory = cert_dir
        )

        self.domain.certificate_updated = datetime.datetime.now()


    def certbot(self, temp, command, *args):
        self.init_temp_dir(temp)
        self.domain.provider.add_credentials(self.domain.config)

        certbot_command = [
            'certbot', command,
            '--agree-tos',
            '--non-interactive',
            '--config-dir', self.root_directory,
            '--work-dir', temp.path('work'),
            '--logs-dir', temp.path('logs')
        ]
        if self.domain.provider_type == 'route53':
            certbot_command.append('--dns-route53')
        else:
            self.command.error("Certbot provider type {} not supported yet".format(self.domain.provider_type))

        command = certbot_command + list(args)
        success = self.command.sh(command,
            cwd = temp.temp_path
        )
        if not success:
            self.command.error("Certbot failed: {}".format(" ".join(command)))

        self.domain.provider.remove_credentials(self.domain.config)
        self.save_certificates(temp)
