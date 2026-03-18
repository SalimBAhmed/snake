from abc import ABC, abstractmethod
from typing import Optional

from snake.settings import get_resolution, calculate_scaled_values, BASE_WIDTH


class CollisionHandler(ABC):
    def __init__(self, next_handler: Optional['CollisionHandler'] = None):
        self._next_handler = next_handler
        
    def set_next(self, handler: 'CollisionHandler') -> 'CollisionHandler':
        self._next_handler = handler
        return handler
        
    @abstractmethod
    def handle(self, game: 'Game', player: 'Player') -> bool:
        if self._next_handler:
            return self._next_handler.handle(game, player)
        return False

class CollisionHandlerFactory:
    @staticmethod
    def create_chain() -> CollisionHandler:
        """Creates the chain of responsibility for collision handling."""
        handler = FoodCollisionHandler()
        handler.set_next(PowerupCollisionHandler()) \
            .set_next(WallCollisionHandler()) \
            .set_next(PlayerCollisionHandler())
        return handler



class FoodCollisionHandler(CollisionHandler):
    def handle(self, game, player) -> bool:
        food = game.food_generator.get(player.player_id, "food")
        if food and player.check_collision(food.position[0], food.position[1]):
            player.grow()
            game.food_generator.destroy(player.player_id, "food")
            
        return super().handle(game, player)


class PowerupCollisionHandler(CollisionHandler):
    def handle(self, game, player) -> bool:
        for powerup_type in ["slow_down"]:  # Add more power-up types as needed
            powerup = game.food_generator.get(player.player_id, powerup_type)
            if powerup and player.check_collision(
                powerup.position[0], powerup.position[1]
            ):
                powerup.apply(player)
                game.food_generator.destroy(player.player_id, powerup_type)
                
        return super().handle(game, player)


class WallCollisionHandler(CollisionHandler):
    def handle(self, game, player) -> bool:
        WINDOW_WIDTH, WINDOW_HEIGHT = get_resolution()
        GAME_WIDTH, GAME_HEIGHT = calculate_scaled_values()
        
        head = player.body[0]
        min_x = 0
        max_x = GAME_WIDTH
        
        if player.player_id == 2:
            min_x = WINDOW_WIDTH - GAME_WIDTH
            max_x = BASE_WIDTH
            
        if head.x < min_x or head.x >= max_x or head.y < 0 or head.y >= GAME_HEIGHT:
            return True
            
        return super().handle(game, player)


class PlayerCollisionHandler(CollisionHandler):
    def handle(self, game, player) -> bool:
        # Self collision
        if player.check_self_collision():
            return True
            
        # # Player-player collision (for multiplayer)
        # for other in game.players:
        #     if other != player and other.check_collision(player.body[0].x, player.body[0].y, include_head=False):
        #         return True
            
        return super().handle(game, player)
