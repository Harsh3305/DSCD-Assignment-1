from src.model.server import Server


class ServerController:

    def __init__(self, port: int, name: str):
        self.server = Server(name=name, address="localhost:" + str(port))
        ## Call reggister server of registry server

    def get_all_client(self):
        pass

    def join_server(self, server_address: str):
        pass
