from src.controller.registry_server_controller import RegistryServerController


def create_controller():
    return RegistryServerController()


def get_all_servers(registry_server_controller: RegistryServerController):
    return registry_server_controller.get_all_server()


if __name__ == "__main__":
    controller = create_controller()
    assert get_all_servers(controller) == []
    pass
