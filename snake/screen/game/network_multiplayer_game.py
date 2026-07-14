import pygame
from snake.player import Player
from snake.network import Client, Server, PlayerData
from time import sleep
from snake.settings import BLACK, calculate_scaled_values, BLOCK_SIZE, get_resolution, RIGHT
from snake.food_generator import FoodGenerator
from snake.collision_handler import CollisionHandlerFactory
from snake.screen import GameScreen
from snake.screen.menu.pause_menu import PauseMenu


class NetworkMultiplayerGame(GameScreen):
    def __init__(self, is_host=False):
        host, port = "127.0.0.1", 5555
        if is_host:
            self.server = Server(host, port)
        self.client = Client(host, port)
        self.food_generator = FoodGenerator()
        self.collision_chain = CollisionHandlerFactory.create_chain()
        self.players = self.setup_players()
        self.started = True


    def setup_players(self):
        GAME_WIDTH, GAME_HEIGHT = calculate_scaled_values()
        WINDOW_WIDTH, WINDOW_HEIGHT = get_resolution()
        starting_position = (GAME_WIDTH // (2 * BLOCK_SIZE)) * BLOCK_SIZE, (GAME_HEIGHT // (2 * BLOCK_SIZE)) * BLOCK_SIZE

        local_id = self.client.player_id

        # Create a temp player to get the full 3-segment starting body
        temp_player = Player(
            self._sprites,
            start_pos=starting_position,
            start_direction=RIGHT,
            player_id=1,
        )
        body_positions = [
            (segment.x, segment.y, segment.direction[0], segment.direction[1])
            for segment in temp_player.body
        ]

        # Send starting position under actual server ID
        player_data = PlayerData(
            server_id=local_id,
            position=body_positions,
            food_pos=None,
            score=0
        )
        players_data = self.client.update_player_data(player_data)
        while not players_data or len(players_data.keys()) < 2:
            players_data = self.client.update_player_data(player_data)
            sleep(0.1)
        self.started = True

        # Local player is self.players[0] (always player_id=1, left screen)
        # Remote player is self.players[1] (always player_id=2, right screen)
        players = []
        players.append(
            Player(
                self._sprites,
                start_pos=starting_position,
                start_direction=RIGHT,
                player_id=1,
            )
        )

        # Initialize the remote player on the right partition
        remote_start = (starting_position[0] + WINDOW_WIDTH - GAME_WIDTH, starting_position[1])
        players.append(
            Player(
                self._sprites,
                start_pos=remote_start,
                start_direction=RIGHT,
                player_id=2,
            )
        )
        return players

    def draw(self, screen):
        screen.fill(BLACK)
        GAME_WIDTH, GAME_HEIGHT = calculate_scaled_values()
        WINDOW_WIDTH, WINDOW_HEIGHT = get_resolution()
        game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        light_green_tile = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        light_green_tile.fill((207, 255, 112))

        dark_green_tile = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        dark_green_tile.fill((60, 163, 112))
        for x in range(0, game_surface.get_width(), BLOCK_SIZE):
            for y in range(0, game_surface.get_height(), BLOCK_SIZE):
                if ((x + y) / BLOCK_SIZE) % 2 == 0:
                    game_surface.blit(light_green_tile, (x, y))
                else:
                    game_surface.blit(dark_green_tile, (x, y))
        screen.blit(game_surface, (0, 0))
        screen.blit(game_surface, (WINDOW_WIDTH - GAME_WIDTH, 0))

        for player in self.players:
            player.draw(screen)
        self.food_generator.draw(screen)

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.context.transition_to(PauseMenu())
            else:
                player = self.players[0]
                player.handle_input(event.key)

    def update(self, clock) -> None:
        GAME_WIDTH, GAME_HEIGHT = calculate_scaled_values()
        WINDOW_WIDTH, WINDOW_HEIGHT = get_resolution()
        if not self.started:
            return
        player = self.players[0]
        player.update(clock.get_time())

        # Check if player can move
        if player.can_move():
            self.food_generator.generate(player.player_id)
            # Check for collisions before moving (food & powerup checks + potential bounds check)
            if self.collision_chain.handle(self, player):
                self.reset(player.player_id)
                return

            # Move the player
            player.move()

            # Check for collisions after moving (food, powerup, walls, self)
            if self.collision_chain.handle(self, player):
                self.reset(player.player_id)
                return

        local_id = self.client.player_id
        remote_id = 3 - local_id

        # Get local player's body coordinates as list of tuples (x, y, dx, dy)
        body_positions = [
            (segment.x, segment.y, segment.direction[0], segment.direction[1])
            for segment in player.body
        ]

        local_food = self.food_generator.get(1, "food")  # Local player is always player_id=1
        local_food_pos = local_food.position if local_food else None

        player_data = PlayerData(
            server_id=local_id,
            position=body_positions,
            food_pos=local_food_pos,
            score=player.score
        )
        players = self.client.update_player_data(player_data)

        if remote_id in players:
            other = players[remote_id]
            from snake.player import Body

            # Reconstruct opponent's body segments on the right partition (add screen offset)
            offset_x = WINDOW_WIDTH - GAME_WIDTH
            self.players[1].body = [
                Body(pos[0] + offset_x, pos[1], (pos[2], pos[3]) if len(pos) >= 4 else RIGHT)
                for pos in other.position
            ]
            self.players[1].score = other.score

            # Update remote food position on the right partition
            remote_food_pos = other.food_pos
            if remote_food_pos:
                remote_food = self.food_generator.get(2, "food")  # Remote player is always player_id=2
                if not remote_food:
                    from snake.food import Food
                    remote_food = Food()
                    self.food_generator._spawned_food[2]["food"] = remote_food
                remote_food.position = (remote_food_pos[0] + offset_x, remote_food_pos[1])
            else:
                self.food_generator.destroy(2, "food")

    def reset(self, player_id: int) -> None:
        self.players = self.setup_players()
