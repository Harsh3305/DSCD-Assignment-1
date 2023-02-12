from src.model.article import Article
from src.model.article_response import ArticleResponse
from src.model.registryServer import RegistryServer
from src.service.client_service import ClientService


class ClientController:
    registry_server_address = RegistryServer.registry_server_address

    def __init__(self, port: int):
        self.service = ClientService(port=port)

    def join_server(self, server_address):
        return self.service.join_server(server_address=server_address)

    def leave_server(self, server_address):
        return self.service.leave_server(server_address=server_address)

    def get_all_join_server(self):
        return self.service.get_all_join_server()

    def choose_current_server(self, server_address):
        return self.service.choose_server(server_address=server_address)

    def get_article(self, article: Article):
        return self.service.get_article(article)

    def post_article(self, article: ArticleResponse):
        return self.service.post_article(article)

    def remove_client(self):
        return self.service.remove_client()

    def is_server_chosen(self):
        return self.service.is_server_chosen()

    def get_chosen_server(self):
        return self.service.get_chosen_server()
