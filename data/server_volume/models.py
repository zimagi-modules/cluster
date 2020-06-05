from systems.models.index import Model, ModelFacade


class ServerVolume(Model('server_volume')):

    def save(self, *args, **kwargs):
        if not isinstance(self.mode, str):
            self.mode = "0{}".format(self.mode)
        super().save(*args, **kwargs)
