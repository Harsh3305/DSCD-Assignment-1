class RegistryServer:
    registry_server_address = ""

    def __init__(self):
        self.servers = []

    def register_address(self, server_address):
        if server_address in self.servers:
            raise Exception("Server already exist")
        else:
            self.servers.append(server_address)
            return "SUCCESS"

    def get_all_server(self):
        return self.servers.copy()

    def remove_server(self, serve_address):
        if serve_address in self.servers:
            self.servers.remove(serve_address)
            return "SUCCESS"
        else:
            raise Exception("Server not found")