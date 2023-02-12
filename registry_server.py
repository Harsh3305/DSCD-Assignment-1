from src.controller.registry_server_controller import RegistryServerController
from src.model.registryServer import RegistryServer

if __name__ == "__main__":
    controller = RegistryServerController()
    print("Registry server is running at " + RegistryServer.registry_server_address)

    input("Press enter to stop this server")
    controller.end()
