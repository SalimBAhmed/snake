from dataclasses import dataclass
from typing import Dict, Tuple, Any
import pygame
from pygame.transform import rotate
from snake.settings import (
    BLOCK_SIZE,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    calculate_scaled_values,
    get_resolution,
)

GAME_WIDTH, GAME_HEIGHT = calculate_scaled_values()
WINDOW_WIDTH, WINDOW_HEIGHT = get_resolution()


@dataclass
class Body:
    x: int
    y: int
    direction: Tuple[int, int]


class Player:
    """Represents a player in the game, handling snake movement and state."""

    # Sprite rotation angles for different directions
    angle = {RIGHT: 270, LEFT: 90, DOWN: 180, UP: 0}

    # Corner sprite rotations for turning
    corner = {
        (UP, RIGHT): 180,
        (UP, LEFT): 90,
        (DOWN, RIGHT): 270,
        (DOWN, LEFT): 0,
        (RIGHT, UP): 0,
        (RIGHT, DOWN): 90,
        (LEFT, UP): 270,
        (LEFT, DOWN): 180,
    }

    def __init__(
        self,
        sprites: Dict[str, Any],
        start_pos: Tuple[int, int] = (100, 100),
        start_direction: Tuple[int, int] = RIGHT,
        player_id: int = 1,
    ):
        """Initialize a new player.

        Args:
            sprites: Dictionary containing sprite images
            start_pos: Starting position (x, y) of the player's head
            start_direction: Starting direction (UP, DOWN, LEFT, RIGHT)
            player_id: Player number (1 or 2)
        """
        self.body = [
            Body(start_pos[0], start_pos[1], start_direction),
            Body(start_pos[0] - BLOCK_SIZE, start_pos[1], start_direction),
            Body(start_pos[0] - 2 * BLOCK_SIZE, start_pos[1], start_direction),
        ]
        self.base_speed = 200
        self.speed = self.base_speed
        self.speed_score = 1
        self.last_move_time = 0
        self.sprites = sprites
        self.score = 0
        self.player_id = player_id
        self.controls = self._get_controls(player_id)

    def _get_controls(self, player_id: int) -> Dict[int, Tuple[int, int]]:
        """Get control scheme based on player ID."""
        if player_id == 1:
            return {
                pygame.K_UP: UP,
                pygame.K_DOWN: DOWN,
                pygame.K_LEFT: LEFT,
                pygame.K_RIGHT: RIGHT,
                pygame.K_w: UP,
                pygame.K_s: DOWN,
                pygame.K_a: LEFT,
                pygame.K_d: RIGHT,
                pygame.K_z: UP,
                pygame.K_q: LEFT,
            }
        else:  # Player 2 controls
            return {
                pygame.K_UP: UP,
                pygame.K_DOWN: DOWN,
                pygame.K_LEFT: LEFT,
                pygame.K_RIGHT: RIGHT,
                pygame.K_i: UP,
                pygame.K_k: DOWN,
                pygame.K_j: LEFT,
                pygame.K_l: RIGHT,
            }

    def handle_input(self, key: int) -> None:
        """Handle keyboard input for this player."""
        if key in self.controls:
            new_direction = self.controls[key]
            # Prevent 180-degree turns
            if (new_direction[0] * -1, new_direction[1] * -1) != self.body[0].direction:
                self.body[0].direction = new_direction

    def update(self, dt: float) -> None:
        """Update the player state based on delta time.

        Args:
            dt: Delta time in milliseconds since last update
        """
        self.last_move_time += dt

    def can_move(self) -> bool:
        """Check if enough time has passed to move the snake.

        Returns:
            True if the player can move, False otherwise
        """
        return self.last_move_time >= self.speed

    def move(self) -> None:
        """Move the player's snake in the current direction."""
        GAME_WIDTH, GAME_HEIGHT = calculate_scaled_values()
        WINDOW_WIDTH, WINDOW_HEIGHT = get_resolution()

        head = self.body[0]
        offset_x = WINDOW_WIDTH - GAME_WIDTH if self.player_id == 2 else 0
        
        # Determine movement relative to their local partition and wrap locally
        rel_x = head.x - offset_x
        new_rel_x = (rel_x + head.direction[0] * BLOCK_SIZE) % GAME_WIDTH
        new_x = new_rel_x + offset_x
        
        new_y = (head.y + head.direction[1] * BLOCK_SIZE) % GAME_HEIGHT
        
        # Create new head and update body
        new_head = Body(new_x, new_y, head.direction)
        self.body = [new_head] + self.body[:-1]
        self.last_move_time = 0

    def grow(self) -> None:
        """Increase the snake's length and update score."""
        self.body.append(
            Body(self.body[-1].x, self.body[-1].y, self.body[-1].direction)
        )
        self.score += 1
        self.speed = max(50, self.base_speed - self.speed_score * 5)
        self.speed_score += 1

    def check_collision(self, x: int, y: int, include_head: bool = True) -> bool:
        """Check if the snake collides with the given position."""
        start = 0 if include_head else 1
        return any(segment.x == x and segment.y == y for segment in self.body[start:])

    def check_self_collision(self) -> bool:
        """Check if the snake's head collides with its body."""
        return any(
            self.body[0].x == segment.x and self.body[0].y == segment.y
            for segment in self.body[1:]
        )

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the player's snake on the screen."""
        GAME_WIDTH, GAME_HEIGHT = calculate_scaled_values()

        if not self.body:
            return

        # Draw head
        head = self.body[0]
        head_sprite = rotate(self.sprites["head"], self.angle[head.direction])
        screen.blit(head_sprite, (head.x, head.y))

        # Draw body segments
        for i in range(1, len(self.body) - 1):
            current = self.body[i]
            next_seg = self.body[i + 1]

            if next_seg.direction == current.direction:
                body_sprite = rotate(
                    self.sprites["body"], self.angle[current.direction]
                )
            else:
                body_sprite = rotate(
                    self.sprites["body_corner"],
                    self.corner.get((current.direction, next_seg.direction), 0),
                )
            screen.blit(body_sprite, (current.x, current.y))

        # Draw tail if there are at least 2 segments
        if len(self.body) > 1:
            tail = self.body[-1]
            tail_sprite = rotate(self.sprites["tail"], self.angle[tail.direction])
            screen.blit(tail_sprite, (tail.x, tail.y))

        font = pygame.font.SysFont("Comic Sans MS", 30)
        score_text = font.render(f"Score: {self.score}", 10, (255, 255, 255))
        screen.blit(score_text, (GAME_WIDTH + 20, 20))

        speed_text = font.render(f"Speed: {self.speed_score}", 10, (255, 255, 255))
        screen.blit(speed_text, (GAME_WIDTH + 20, 50))
