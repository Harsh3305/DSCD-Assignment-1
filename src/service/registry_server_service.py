from src.repository.registry_server_repository import RegistryServeRepository


class RegistryServerService:

    def get_registry_server_address(self):
        return get_registry_server_address()

    def __init__(self):
        self.repository = RegistryServeRepository()

    def get_all_server(self):
        return self.repository.get_all_server()

    def end(self):
        return self.repository.end()
