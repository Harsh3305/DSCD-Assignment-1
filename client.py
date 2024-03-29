from src.controller.client_controller import ClientController
from src.model.article import Article
from src.model.article_response import ArticleResponse


def convert_to_none(data):
    if data == "":
        return None
    else:
        return data

def type_cast_to_null(data: str):
    if data is None:
        return "<BLANK>"
    else:
        return data

if __name__ == "__main__":
    port = int(input("Enter Port Number: "))
    print("Creating a client with port number " + str(port))

    controller = ClientController(port=port)

    isEnded = False
    while not isEnded:
        if controller.is_server_chosen():
            print("Selected server is " + controller.get_chosen_server())
            print("Select an operation")
            print("1) Post an article")
            print("2) Get articles from selected server")
            print("3) Go a step back")
            selected_option = int(input(" Selected option is: "))

            if selected_option == 1:
                type = convert_to_none(input("Enter type of article\n"))
                author = convert_to_none(input("Enter author of article \n"))
                content = convert_to_none(input("Enter content of article \n"))

                if author is None:
                    print("author cannot be empty")
                else:
                    article = ArticleResponse(Content=content, Author=author, Type=type, Date="2023-02-12")
                    response = controller.post_article(article=article)
                    print(response)

            elif selected_option == 2:
                type = convert_to_none(input("Enter type to filter articles\n"))
                author = convert_to_none(input("Enter author to filter articles \n"))
                date = convert_to_none(input("Enter date to filter articles \n"))
                print(
                    "For " + type_cast_to_null(type) + ", " + type_cast_to_null(author) + ", " + type_cast_to_null(date)
                )
                article = Article(
                    Type=type,
                    Author=author,
                    Date=date
                )

                try:
                    response = controller.get_article(article=article)
                    print(response)
                except Exception as e:
                    print("FAIL")
            else:
                controller.choose_current_server("")
        else:
            print("Select an operation")
            print("1) Get all available servers")
            print("2) Get joined servers")
            print("3) Join a server")
            print("4) Leave a server")
            print("5) Choose a server to do operation")
            print("6) Exit program")

            selected_option = int(input(" Selected option is: "))

            if selected_option == 1:
                servers = controller.get_all_servers()
                for server in servers:
                    print(server)
            elif selected_option == 2:
                print(controller.get_all_join_server())
            elif selected_option == 3:
                address = input("Enter server address which you want to join: ")
                controller.join_server(address)
            elif selected_option == 4:
                address = input("Enter server address which you want to leave: ")
                controller.leave_server(address)
            elif selected_option == 5:
                address = input("Enter server address which you want to use for operations: ")
                controller.choose_current_server(address)
            else:
                isEnded = True
