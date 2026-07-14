from dataclasses import dataclass


@dataclass
class PlayerData:
    server_id: int | None
    position: list
    food_pos: tuple[int, int] | None
    score: int

    def to_dict(self):
        return {
            "server_id": self.server_id,
            "position": self.position,
            "food_pos": self.food_pos,
            "score": self.score,
        }
