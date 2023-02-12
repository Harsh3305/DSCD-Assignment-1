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

        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect(address)
        socket.subscribe("JOIN_SERVER")
        socket.subscribe("LEAVE_SERVER")
        socket.subscribe("GET_ARTICLE")
        socket.subscribe("PUBLISH_ARTICLE")

        self.socket = socket

        threading.Thread(target=self.accept_messages).start()

    def accept_messages(self):
        while not self.destroy:
            req = self.socket.recv_string()
            data = self.socket.recv_json()
            print({
                "req":req,
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
                    ))
                elif req == 'PUBLISH_ARTICLE':
                    res = self.publish_article(ArticleResponse(
                        Author=data["Author"],
                        Date=data["Date"],
                        Type=data["Type"],
                        Content=data["Content"]
                    ))
                else:
                    return "FAIL"
                self.response(tag=req, client_address=data["client_address"], response=res)
            except Exception as e:
                print(e)
                self.response(tag=req, client_address=data["client_address"], response="FAIL")
                ## Send FAIL

            # time.sleep(0.5)
    def response(self, tag: str, client_address: str, response):

        socket = zmq.Context()
        socket = socket.socket(zmq.PUB)
        socket.bind(client_address)
        time.sleep(5)
        tag = "RESPONSE_"+tag
        socket.send_string(tag, flags=zmq.SNDMORE)
        socket.send_json(response)
        socket.disconnect(client_address)

    def accept_connection_request(self, client_uuid: str, client_address: str):
        if len(self.CLIENTELE) > Server.MAX_CLIENT:
            raise Exception("Client limit reach for this server")
        elif client_uuid in self.CLIENTELE:
            raise Exception("Client is already a member of this server")
        else:
            self.CLIENTELE[client_uuid] = client_address
            return "SUCCESS"

    def leave_client(self, client_uuid: str):
        if client_uuid in self.CLIENTELE:
            del self.CLIENTELE[client_uuid]
            return "SUCCESS"
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
        # TODO:
        pass
