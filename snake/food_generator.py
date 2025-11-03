import random
from snake.food import Food
from snake.power_up import SlowDown
from copy import deepcopy

class FoodGenerator:
    _FOOD_RATE = 1
    _SLOW_DOWN_RATE = 0.005
    _FOOD_TYPES = {"food": Food, "slow_down": SlowDown}
    _spawned_food = {1: {}, 2: {}}

    def generate(self, player_id):
        for food_type in self._FOOD_TYPES.keys():
            if food_type in self._spawned_food[player_id]:
                continue
            if random.random() < getattr(self, f"_{food_type.upper()}_RATE"):
                food_class = self._FOOD_TYPES[food_type]
                food = food_class()
                food.spawn(player_id)
                self._spawned_food[player_id][food_type] = food

    def destroy(self, player_id=None, food_type=None):
        _spawned_food_copy = deepcopy(self._spawned_food)
        if not player_id:
            for player_id in _spawned_food_copy.keys():
                self.destroy(player_id, food_type)
            return
        for food in _spawned_food_copy[player_id].keys():
            if food == food_type or not food_type:
                del self._spawned_food[player_id][food]

    def draw(self, screen):
        for player_id in self._spawned_food.keys():
            for food in self._spawned_food[player_id].values():
                food.draw(screen)

    def __getitem__(self, key):
        if key not in self._spawned_food:
            raise KeyError(key)
        return self._spawned_food[key]
    
    def get(self, player_id, key, default=None):
        return self._spawned_food.get(player_id, {}).get(key, default)