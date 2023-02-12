from src.controller.server_controller import ServerController

if __name__ == "__main__":
    port = int(input("Enter Port Number: "))
    name = input("Enter Server Name: ")
    print("Creating a server with port number " + str(port) + " and with name " + name)

    controller = ServerController(port, name=name)
    input("Press enter to end this: ")
    controller.get_all_client()
    controller.end()
