from src.repository.registry_server_repository import RegistryServeRepository


class RegistryServerService:

    def __init__(self):
        self.repository = RegistryServeRepository()

    def get_all_server(self):
        return self.repository.get_all_server()
