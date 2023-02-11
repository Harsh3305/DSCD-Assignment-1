from src.model.article import Article
from src.model.article_response import ArticleResponse


class Server:
    MAX_CLIENT = 10

    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.CLIENTELE = {}
        self.articles = []

    def accept_connection_request(self, client):
        if len(self.CLIENTELE) > Server.MAX_CLIENT:
            raise Exception("Client limit reach for this server")
        elif client.uuid in self.CLIENTELE:
            raise Exception("Client is already a member of this server")
        else:
            self.CLIENTELE[client.uuid] = client

    def leave_client(self, client_uuid: str):
        if client_uuid in self.CLIENTELE:
            del self.CLIENTELE[client_uuid]
        else:
            raise Exception("Client is not a member of this server")

    def get_articles(self, article: Article):
        process_articles = self.articles.copy()
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

    def publish_article(self, article: ArticleResponse):
        self.articles.append(article)
        return "SUCCESS"

    def join_server(self):
        pass
