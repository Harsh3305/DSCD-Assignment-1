import threading
import time

import zmq


class RegistryServer:
    registry_server_address = "tcp://127.0.0.1:8080"

    def __init__(self):
        self.servers = []
        subs_socker = zmq.Context().socket(zmq.SUB)
        print("Connecting to " + RegistryServer.registry_server_address)
        subs_socker.connect(RegistryServer.registry_server_address)
        subs_socker.subscribe("REGISTER_SERVER")
        subs_socker.subscribe("GET_ALL_SERVERS")
        self.is_end = False

        self.subs_socker = subs_socker

        # pub_socker = zmq.Context().socket(zmq.PUB)
        # pub_socker.connect(RegistryServer.registry_server_address)
        #
        # self.pub_socker = pub_socker
        threading.Thread(target=self.listen).start()

    def listen(self):
        while not self.is_end:
            print("Waiting for query")
            req = self.subs_socker.recv_string()
            data = self.subs_socker.recv_json()
            res = "SUCCESS"
            try:
                if req == "REGISTER_SERVER":
                    res = self.register_address(data["address"], data["name"])
                elif req == "GET_ALL_SERVERS":
                    res = self.get_all_server(data["address"])
            except Exception as e:
                print(e)
                res = "FAIL"
            print({
                "req": req,
                "res": res
            })
            try:
                self.response(data["address"], req, res)
            except Exception as e:
                print(e)

    def response(self, address, tag: str, res):
        socket = zmq.Context().socket(zmq.PUB)
        socket.bind(address)
        time.sleep(5)
        socket.send_string("RESPONSE_" + tag, flags=zmq.SNDMORE)
        socket.send_json(res)
        socket.disconnect(address)

    def register_address(self, server_address: str, name: str):
        # Logging
        print("JOIN REQUEST FROM " + server_address)
        if server_address in self.servers:
            raise Exception("Server already exist")
        else:
            self.servers.append({
                "address": server_address,
                "name": name
            })
            return "SUCCESS"

    def get_all_server(self, client_address):
        # Logging
        print("SERVER LIST REQUEST FROM " + client_address)
        return self.servers.copy()

    def remove_server(self, serve_address):
        if serve_address in self.servers:
            self.servers.remove(serve_address)
            return "SUCCESS"
        else:
            raise Exception("Server not found")
