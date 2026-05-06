import random

import pygame

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH
from logger import log_event


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

    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")

        angle = random.uniform(20, 50)
        velocity_one = self.velocity.rotate(angle)
        velocity_two = self.velocity.rotate(-angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS

        asteroid_1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_2 = Asteroid(self.position.x, self.position.y, new_radius)

        asteroid_1.velocity = velocity_one * 1.2
        asteroid_2.velocity = velocity_two * 1.2
