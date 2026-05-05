import pygame

from circleshape import CircleShape
from constants import LINE_WIDTH


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        surface = screen
        color = "white"
        center = self.position
        radius = self.radius
        line_width = LINE_WIDTH

        pygame.draw.circle(surface, color, center, radius, line_width)

    def update(self, dt):
        self.position += self.velocity * dt
