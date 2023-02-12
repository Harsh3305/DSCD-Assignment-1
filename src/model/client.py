import uuid

import zmq

from src.model.article import Article
from src.model.article_response import ArticleResponse
from src.model.registryServer import RegistryServer


class Client:

    def __init__(self, address: str):
        self.uuid = str(uuid.uuid1())
        self.address = address
        self.join_server_address = []

    def join_server(self, server_address: str):
        if server_address in self.join_server_address:
            return Exception("Server was already joined")
        else:
            self.join_server_address.append(server_address)

    def leave_server(self, server_address):
        if server_address not in self.join_server_address:
            raise Exception("First join server")
        else:
            ## TODO: Remove server
            self.join_server_address.remove(server_address)

    def get_articles(self, article: Article):
        pass

    def publish_article(self, article: ArticleResponse):
        pass

    def get_all_registered_server(self):
        return self.join_server_address.copy()
