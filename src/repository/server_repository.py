from src.model.server import Server


class ServerRepository:
    def __init__(self, port: int, name: str):
        self.server = Server(name=name, address="localhost:" + str(port))

    def get_all_client(self):
        pass

    def join_server(self, server_address: str):
        pass
