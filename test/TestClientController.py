from src.controller.client_controller import ClientController
from src.model.article import Article
from src.model.article_response import ArticleResponse


def create_controller(port):
    return ClientController(port=port)


def join_serve(client_controller: ClientController, server_address: str):
    return client_controller.join_server(server_address=server_address)


def leave_server(client_controller: ClientController, server_address: str):
    return client_controller.leave_server(server_address=server_address)


def get_all_join_server(client_controller: ClientController):
    return client_controller.get_all_join_server()


def choose_current_serve(server_address: str, client_controller: ClientController):
    return client_controller.choose_current_server(server_address=server_address)


def get_article(client_controller: ClientController, article: Article):
    return client_controller.get_article(article=article)


def post_article(client_controller: ClientController, article: ArticleResponse):
    return client_controller.post_article(article=article)


def remove_client(client_controller: ClientController):
    return client_controller.remove_client()


if __name__ == "__main__":
    controller1 = create_controller(3000)
    assert join_serve(controller1, "random_address") == "SUCCESS"
    assert leave_server(controller1, "random_address") == "SUCCESS"
    assert leave_server(controller1, "random_address") == "FAIL"
    assert get_all_join_server(controller1) == []

    controller2 = create_controller(3001)
    assert join_serve(controller2, "server_address_1") == "SUCCESS"
    assert get_all_join_server(controller2) == ["server_address_1"]
    assert join_serve(controller2, "server_address_2") == "SUCCESS"
    assert choose_current_serve("server_address_1", controller2) == "SUCCESS"
