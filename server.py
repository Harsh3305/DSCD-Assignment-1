from src.controller.server_controller import ServerController

if __name__ == "__main__":
    port = int(input("Enter Port Number: "))
    name = input("Enter Server Name: ")
    print("Creating a server with port number " + str(port) + " and with name " + name)

    controller = ServerController(port, name=name)

    while True:
        address = input("Enter server address which you want to join: \n")
        print(controller.join_server(server_address=address))
    # controller.get_all_client()
    # controller.end()
