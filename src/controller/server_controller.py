from src.service.server_service import ServerService


class ServerController:

    def __init__(self, port: int, name: str):
        self.service = ServerService(name=name, address="localhost:" + str(port))
        # Call register server of registry server

    def get_all_client(self):
        return self.service.get_all_client()

    def join_server(self, server_address: str):
        return self.service.join_server(server_address=server_address)
