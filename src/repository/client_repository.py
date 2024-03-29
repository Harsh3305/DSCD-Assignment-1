import time

import zmq

from src.model.client import Client
from src.model.article_response import ArticleResponse
from src.model.article import Article
from src.model.registryServer import RegistryServer


class ClientRepository:
    def __init__(self, port: int):
        self.client = Client(address="tcp://127.0.0.1:" + str(port))
        self.current_server = ""

    def is_server_chosen(self):
        return not self.current_server == ""

    def request(self, tag: str, server_address: str, payload):

        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind(server_address)
        time.sleep(1)
        socket.send_string(tag, flags=zmq.SNDMORE)
        socket.send_json(payload)

    def response(self, tag: str):
        # time.sleep(5)
        socker_response = zmq.Context()
        socker_response = socker_response.socket(zmq.SUB)
        socker_response.connect(self.client.address)
        # time.sleep(1)
        tag = "RESPONSE_" + tag
        socker_response.subscribe(tag)
        res = socker_response.recv_string()
        data = socker_response.recv_json()
        print(data)

        return data

    def join_server(self, server_address):
        try:
            self.client.join_server(server_address=server_address)

            tag = "JOIN_SERVER"
            self.request(tag, server_address=server_address, payload={
                "client_uuid": self.client.uuid,
                "client_address": self.client.address
            })
            self.response(tag)
            return "SUCCESS"
        except Exception as e:
            return "FAIL"

    def leave_server(self, server_address):
        try:
            self.client.leave_server(server_address=server_address)
            tag = "LEAVE_SERVER"
            self.request(tag, server_address=server_address, payload={
                "client_uuid": self.client.uuid,
                "client_address": self.client.address
            })
            self.response(tag)
            return "SUCCESS"
        except Exception as e:
            return "FAIL"

    def get_all_join_server(self):
        return self.client.get_all_registered_server()

    def choose_server(self, server_address):
        if server_address == "":
            self.current_server = server_address
        elif server_address in self.get_all_join_server():
            self.current_server = server_address
            return "SUCCESS"
        else:
            return "FAIL"

    def get_article(self, article: Article):
        tag = "GET_ARTICLE"
        self.request(tag, server_address=self.current_server, payload={
            "client_uuid": self.client.uuid,
            "client_address": self.client.address,
            "Type": article.Type,
            "Date": article.Date,
            "Author": article.Author
        })

        data = self.response(tag)

        for i in range(len(data)):
            raw_article = data[i]
            print(str(i+1) + ")"+str(raw_article["Type"]))
            print(str(raw_article["Author"]))
            print(str(raw_article["Date"]))
            print(str(raw_article["Content"]))

    def post_article(self, article: ArticleResponse):
        tag = "PUBLISH_ARTICLE"
        self.request(tag, server_address=self.current_server, payload={
            "client_uuid": self.client.uuid,
            "client_address": self.client.address,
            "Type": article.Type,
            "Date": article.Date,
            "Author": article.Author,
            "Content": article.Content
        })
        self.response(tag)

    def get_all_server(self):

        pub_socket = zmq.Context().socket(zmq.PUB)
        pub_socket.bind(RegistryServer.registry_server_address)
        time.sleep(1)
        pub_socket.send_string("GET_ALL_SERVERS", flags=zmq.SNDMORE)
        pub_socket.send_json({
            "address": self.client.address,
            "uuid": self.client.uuid,
        })
        # pub_socket.disconnect(RegistryServer.registry_server_address)

        sub_socket = zmq.Context().socket(zmq.SUB)
        sub_socket.connect(self.client.address)
        time.sleep(1)
        sub_socket.subscribe("RESPONSE_GET_ALL_SERVERS")
        req = sub_socket.recv_string()
        data = sub_socket.recv_json()
        print({
            "req": req,
            "res": data
        })
        new_data = []
        for d in data:
            new_data.append(d["name"] + " - " + d["address"])
        return new_data
