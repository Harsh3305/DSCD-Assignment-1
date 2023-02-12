from src.repository.server_repository import ServerRepository


class ServerService:

    def __init__(self, port: int, name: str):
        self.repository = ServerRepository(port=port, name=name)

    def get_all_client(self):
        return self.repository.get_all_client()

    def join_server(self, server_address: str):
        return self.repository.join_server(server_address=server_address)

    def end(self):
        return self.repository.end()
