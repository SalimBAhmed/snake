import json
import socket
import sys
from snake.network.models import PlayerData

class Network:
    def __init__(self, server="0.0.0.0", port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = port
        self.addr = (self.server, self.port)

    def accept(self):
        return self.client.accept()

    def bind(self):
        try:
            self.client.bind(self.addr)
            print("Bound to server")
        except socket.error as msg:
            print(msg)
            sys.exit()
        self.client.listen(2)

    def connect(self) -> int | None:
        try:
            self.client.connect(self.addr)
            reply = self.recv(2048)
            if reply and "Connected" in reply:
                player_id = int(reply.split(",")[1].split("=")[1])
                print(f"Connected to server, player_id={player_id}")
                return player_id
        except:
            pass

    def recv(self, bufsize=4096) -> str | None:
        try:
            return self.client.recv(bufsize).decode()
        except socket.error as e:
            print(e)
            return None

    def send(self, data, bufsize=4096):
        try:
            self.client.send(str.encode(data))
            return self.recv(bufsize)
        except socket.error as e:
            print(e)

    def serialize(self, data):
        return json.dumps(data)

    def deserialize(self, data):
        return json.loads(data)
