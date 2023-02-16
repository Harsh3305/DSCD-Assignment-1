import threading
import time

import zmq

from src.model.article import Article
from src.model.article_response import ArticleResponse


class Server:
    MAX_CLIENT = 10

    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.CLIENTELE = {}
        self.articles = []
        self.destroy = False
        self.joined_server = []

        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect(address)
        socket.subscribe("JOIN_SERVER")
        socket.subscribe("LEAVE_SERVER")
        socket.subscribe("GET_ARTICLE")
        socket.subscribe("PUBLISH_ARTICLE")
        socket.subscribe("SERVER_GET_ARTICLE")
        socket.subscribe("GET_SERVER_ADDRESS")
        self.socket = socket

        threading.Thread(target=self.accept_messages).start()

    def accept_messages(self):
        while not self.destroy:
            req = self.socket.recv_string()
            data = self.socket.recv_json()
            print({
                "req": req,
                "data": data
            })
            try:
                if req == 'JOIN_SERVER':
                    res = self.accept_connection_request(data["client_uuid"], data["client_address"])
                elif req == 'LEAVE_SERVER':
                    res = self.leave_client(data["client_uuid"])
                elif req == 'GET_ARTICLE':
                    res = self.get_articles(Article(
                        Author=data["Author"],
                        Date=data["Date"],
                        Type=data["Type"]
                    ), client_uuid=data["client_uuid"])
                    res = [article.to_json() for article in res]
                elif req == 'PUBLISH_ARTICLE':
                    res = self.publish_article(ArticleResponse(
                        Author=data["Author"],
                        Date=data["Date"],
                        Type=data["Type"],
                        Content=data["Content"]
                    ), client_uuid=data["client_uuid"])
                elif req == "SERVER_GET_ARTICLE":
                    res = self.get_articles_for_server()
                elif req == "GET_SERVER_ADDRESS":
                    res = self.get_server_join_address()
                else:
                    return "FAIL"
                self.response(tag=req, client_address=data["client_address"], response=res)
            except Exception as e:
                print(e)
                self.response(tag=req, client_address=data["client_address"], response="FAIL")
                # Send FAIL

            # time.sleep(0.5)

    def response(self, tag: str, client_address: str, response):

        socket = zmq.Context()
        socket = socket.socket(zmq.PUB)
        socket.bind(client_address)
        time.sleep(5)
        tag = "RESPONSE_" + tag
        socket.send_string(tag, flags=zmq.SNDMORE)
        socket.send_json(response)
        socket.disconnect(client_address)

    def accept_connection_request(self, client_uuid: str, client_address: str):
        # Logging
        print("JOIN REQUEST FROM " + client_uuid)
        if len(self.CLIENTELE) > Server.MAX_CLIENT:
            raise Exception("Client limit reach for this server")
        elif client_uuid in self.CLIENTELE:
            raise Exception("Client is already a member of this server")
        else:
            self.CLIENTELE[client_uuid] = client_address
            return "SUCCESS"

    def leave_client(self, client_uuid: str):
        # Logging
        print("LEAVE REQUEST FROM " + client_uuid)
        if client_uuid in self.CLIENTELE:
            del self.CLIENTELE[client_uuid]
            return "SUCCESS"
        else:
            raise Exception("Client is not a member of this server")

    def get_articles(self, article: Article, client_uuid: str):
        # Logging
        print("GET ARTICLE REQUEST FROM " + client_uuid) ##TODO: CORRECT THIS
        articles = self.get_articles_from_other_serves()
        process_articles = self.articles.copy() + articles
        if article.Type is not None:
            process_articles = [
                filtered_article for filtered_article in process_articles if filtered_article.Type == article.Type
            ]
        if article.Author is not None:
            process_articles = [
                filtered_article for filtered_article in process_articles if filtered_article.Type == article.Type
            ]
        if article.Date is not None:
            process_articles = [
                filtered_article for filtered_article in process_articles if filtered_article.Date >= article.Date
            ]
        return process_articles

    def publish_article(self, article: ArticleResponse, client_uuid: str):
        # Logging
        print("ARTICLE PUBLISH FROM " + client_uuid)
        self.articles.append(article)
        return "SUCCESS"

    def join_server(self, address: str):
        if address in self.joined_server:
            raise Exception("Server already exist in join_server list")
        else:
            self.joined_server.append(address)
            return "SUCCESS"

    def join_server_request(self):
        return self.joined_server.copy()

    def get_articles_for_server(self):
        return [raw_article.to_json() for raw_article in self.articles.copy()]
    
    def add_server_address(self, addresses: list):
        for address in addresses:
            if address not in self.joined_server:
                self.joined_server.append(address)
        return "SUCCESS"

    def get_server_join_address(self):
        return self.joined_server.copy()

    def sync_jon_servers(self):
        temp_joined_servers = self.joined_server.copy()
        for address in temp_joined_servers:
            socket = zmq.Context().socket(zmq.PUB)
            socket.bind(address)
            time.sleep(1)
            socket.send_string("GET_SERVER_ADDRESS", flags=zmq.SNDMORE)
            socket.send_json({
                "client_address": self.address
            })

            socket = zmq.Context().socket(zmq.SUB)
            socket.connect(self.address)
            time.sleep(1)
            socket.subscribe("RESPONSE_GET_SERVER_ADDRESS")
            req = socket.recv_string()
            data = socket.recv_json()

            for child_servers in data:
                if child_servers not in temp_joined_servers and child_servers != self.address:
                    temp_joined_servers.append(child_servers)

        return temp_joined_servers

    def get_articles_from_other_serves(self):
        temp_joined_servers = self.sync_jon_servers()
        articles = []
        for address in temp_joined_servers:
            socket = zmq.Context().socket(zmq.PUB)
            socket.bind(address)
            time.sleep(1)
            socket.send_string("SERVER_GET_ARTICLE", flags=zmq.SNDMORE)
            socket.send_json({
                "client_address": self.address
            })

            socket = zmq.Context().socket(zmq.SUB)
            socket.connect(self.address)
            time.sleep(1)
            socket.subscribe("RESPONSE_SERVER_GET_ARTICLE")
            req = socket.recv_string()
            data = socket.recv_json()

            for raw_article in data:
                print(raw_article)
                article = ArticleResponse.from_json(raw_article)
                articles.append(article)

        return articles