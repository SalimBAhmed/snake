import pygame
from snake.network import Network
from snake.network.models import PlayerData

class Client(Network):
    def __init__(self, server, port):
        super().__init__(server, port)
        self.player_id = self.connect()

    def update_player_data(self, player_data) -> dict:
        player_data.server_id = self.player_id
        message = f"update_player:{self.serialize(player_data.to_dict())}"
        print("Client Sending:", message)
        reply = self.send(message)
        print("Client Received:", reply)
        if not reply:
            return {}
        players_dict = self.deserialize(reply)
        players = {}
        for player_id_str, p_info in players_dict.items():
            player_id = int(player_id_str)
            players[player_id] = PlayerData(**p_info)
        print("new", players)
        return players
