from settings.roles import Roles
from .storage import StorageRouterCommand, StorageActionCommand


class MountRouterCommand(StorageRouterCommand):

    def get_priority(self):
        return 40


class MountActionCommand(StorageActionCommand):

    def get_priority(self):
        return 40

