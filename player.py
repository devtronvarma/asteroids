import pygame

from circleshape import CircleShape
from constants import LINE_WIDTH, PLAYER_RADIUS


class Player(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius=PLAYER_RADIUS)
        self.rotation = 0

    # in the Player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        color = "white"
        points = self.triangle()
        line_width = LINE_WIDTH
        pygame.draw.polygon(screen, color, points, line_width)
