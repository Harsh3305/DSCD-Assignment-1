from src.service.registry_server_service import RegistryServerService


class RegistryServerController:

    def __init__(self):
        self.service = RegistryServerService()

    # def get_all_server(self):
    #     return self.service.get_all_server()
    #

    def get_address_of_registry_server(self):
        self.service.get_registry_server_address()

    def end(self):
        return self.service.end()
