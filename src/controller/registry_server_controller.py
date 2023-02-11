from src.service.registry_server_service import RegistryServerService


class RegistryServerController:

    def __init__(self):
        self.service = RegistryServerService()

    def get_all_server(self):
        return self.service.get_all_server()
