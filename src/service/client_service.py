from src.model.article import Article
from src.model.article_response import ArticleResponse
from src.repository.client_repository import ClientRepository


class ClientService:
    def __init__(self, port: int):
        self.repository = ClientRepository(port=port)

    def join_server(self, server_address):
        return self.repository.join_server(server_address=server_address)

    def leave_server(self, server_address):
        return self.repository.leave_server(server_address=server_address)

    def get_all_join_server(self):
        return self.repository.get_all_join_server()

    def choose_server(self, server_address):
        return self.repository.choose_server(server_address=server_address)

    def get_article(self, article: Article):
        return self.repository.get_article(article=article)

    def post_article(self, article: ArticleResponse):
        return self.repository.post_article(article=article)

    def remove_client(self):
        for server in self.get_all_join_server():
            self.leave_server(server.address)
        return "SUCCESS"

    def is_server_chosen(self):
        return self.repository.is_server_chosen()

    def get_chosen_server(self):
        return self.repository.current_server

    def get_all_servers(self):
        return self.repository.get_all_server()
