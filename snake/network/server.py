import threading
from snake.network import Network
from concurrent.futures import ThreadPoolExecutor
from snake.network.models import PlayerData
class Server(Network):
    def __init__(self, server, port):
        super().__init__(server, port)
        self.players = {}
        self.executor = ThreadPoolExecutor()
        self.executor.submit(self.start)

    def start(self):
        self.bind()
        threads = []
        # TODO: Change while True to while game is running
        while True:
            conn, addr = self.accept()
            player_id = len(self.players.keys()) + 1
            self.players[player_id] = {
                "addr": addr,
                "server_id": player_id,
                "position": [],
                "food_pos": None,
                "score": 0,
            }
            print("Connected to:", addr, "players:", player_id)
            threads.append(threading.Thread(target=self.threaded_client, args=(conn,)))
            threads[-1].start()
            threads = [t for t in threads if t.is_alive()]
        self.executor.shutdown()

    def threaded_client(self, conn):
        conn.send(str.encode(f"Connected, player_id={len(self.players.keys())}"))
        reply = ""
        while True:
            try:
                reply = ""
                data = conn.recv(2048).decode("utf-8")
                print("Server Received:", data)
                if not data:
                    break
                elif data.startswith("update_player"):
                    player_dict = self.deserialize(data[len("update_player:"):])
                    player_id = player_dict.get("server_id")
                    if player_id in self.players:
                        self.players[player_id].update(player_dict)

                    reply_data = {
                        p_id: {k: v for k, v in p_info.items() if k != "addr"}
                        for p_id, p_info in self.players.items()
                    }
                    reply = self.serialize(reply_data)
                print("Server Sending:", reply)
                conn.sendall(reply.encode("utf-8"))
            except Exception as e:
                print("Server client thread error:", e)
                break
        print("Connection closed")
        conn.close()

    def get_players(self):
        return self.players

    def update_player(self, addr, data):
        if addr in self.players:
            self.players[addr] = data
