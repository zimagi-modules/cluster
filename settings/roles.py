
class Roles(object, metaclass = MetaRoles):
    index = {
        # Network roles
        'network-admin': "Network administrator (full privileges over all environment networks, subnets, and firewalls)",
        'security-admin': "Network security administrator (full privileges over environment firewalls)",

        # Server roles
        'server-admin': "Server administrator (full privileges over all environment servers)",

        # Storage roles
        'storage-admin': "Storage administrator (full privileges over all environment storage mounts)"
    }
