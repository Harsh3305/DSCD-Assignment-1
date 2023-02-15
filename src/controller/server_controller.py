import time

import zmq

from src.model.registryServer import RegistryServer
from src.service.server_service import ServerService


class ServerController:

    def __init__(self, port: int, name: str):
        self.service = ServerService(name=name, port=port)
        # Call register server of registry server
        socket = zmq.Context().socket(zmq.PUB)
        socket.bind(RegistryServer.registry_server_address)
        time.sleep(1)
        socket.send_string("REGISTER_SERVER", flags=zmq.SNDMORE)
        socket.send_json({
            "address": self.service.get_address(),
            "name": name
        })

        socket = zmq.Context().socket(zmq.SUB)
        socket.connect(self.service.get_address())
        time.sleep(1)
        socket.subscribe("RESPONSE_REGISTER_SERVER")
        req = socket.recv_string()
        data = socket.recv_json()
        print(data)


    def get_all_client(self):
        return self.service.get_all_client()

    def join_server(self, server_address: str):
        return self.service.join_server(server_address=server_address)

    def end(self):
        return self.service.end()
