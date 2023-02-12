from src.controller.client_controller import ClientController
if __name__ == "__main__":

    print("erger")

    controller = ClientController(8081)
    controller.join_server("tcp://127.0.0.1:"+str(8080))
    controller.leave_server("tcp://127.0.0.1:"+str(8080))
