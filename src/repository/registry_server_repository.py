from src.model.registryServer import RegistryServer


class RegistryServeRepository:

    def __init__(self):
        self.registry_server = RegistryServer()

    def get_all_server(self):
        return self.registry_server.get_all_server()

    def register_server(self, server_address: str):
        self.registry_server.register_address(server_address=server_address)
        # TODO: add call
        return "SUCCESS"

    def end(self):
        self.registry_server.is_end = True
        return "SUCCESS"
