from src.model.client import Client
from src.model.article_response import ArticleResponse
from src.model.article import Article


class ClientRepository:
    def __init__(self, port: int):
        self.client = Client(address="localhost:" + str(port))
        self.current_server = ""

    def join_server(self, server_address):
        try:
            self.client.join_server(server_address=server_address)
            ## TODO: Join server
            return "SUCCESS"
        except Exception as e:
            return "FAIL"

    def leave_server(self, server_address):
        try:
            self.client.leave_server(server_address=server_address)
            ## TODO: Leave server
            return "SUCCESS"
        except Exception as e:
            return "FAIL"

    def get_all_join_server(self):
        return self.client.get_all_registered_server()

    def choose_server(self, server_address):
        self.current_server = server_address
        return "SUCCESS"

    def get_article(self, article: Article):
        pass

    def post_article(self, article: ArticleResponse):
        pass
