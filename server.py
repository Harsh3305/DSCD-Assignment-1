from src.controller.server_controller import ServerController

if __name__ == "__main__":
    controller = ServerController(8080, "test")
    input("Press enter to end this: ")
    controller.get_all_client()
    controller.end()
