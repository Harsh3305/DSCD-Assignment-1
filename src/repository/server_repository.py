import time

import zmq

from src.model.server import Server


class ServerRepository:
    def __init__(self, port: int, name: str):
        self.server = Server(name=name, address="tcp://127.0.0.1:" + str(port))
        self.clients = []

    def get_all_client(self):
        return self.clients.copy()

    def join_server(self, server_address: str):
        try:
            return self.server.join_server(address=server_address)
        except Exception as e:
            print(e)
            return "FAIL"

    def end(self):
        self.server.destroy = True
        return "SUCCESS"

    def get_address(self):
        return self.server.address
