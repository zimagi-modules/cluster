from systems.models.index import Model, ModelFacade


class ServerFacade(ModelFacade('server')):

    def get_field_password_display(self, instance, value, short):
        if not value:
            return None

        if short:
            return self.encrypted_color('*****')
        return self.encrypted_color(value)

    def get_field_private_key_display(self, instance, value, short):
        if not value:
            return None

        if short:
            return self.encrypted_color('*****')
        return self.encrypted_color(value)

    def get_field_status_display(self, instance, value, short):
        if value == self.model.STATUS_RUNNING:
            return self.success_color(value)
        return self.error_color(value)


class Server(Model('server')):

    STATUS_RUNNING = 'running'
    STATUS_UNREACHABLE = 'unreachable'

    @property
    def ip(self):
        return self.public_ip if self.public_ip else self.private_ip

    @property
    def status(self):
        return self.STATUS_RUNNING if self.ping() else self.STATUS_UNREACHABLE

    def running(self):
        if self.status == self.STATUS_RUNNING:
            return True
        return False


    def ping(self):
        return self.provider.ping()

    def start(self):
        return self.provider.start()

    def stop(self):
        return self.provider.stop()
