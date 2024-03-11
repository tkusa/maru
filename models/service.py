

class Service:

    def __init__(self, protocol, name, port) -> None:
        self.protocol = protocol
        self.name = name
        self.port = port
        self.endpoints = []
