import random

import pygame

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH
from logger import log_event


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.bug_kind = random.choice(("beetle", "ladybug", "roach"))
        self.rotation = random.randrange(360)
        self.rotation_speed = random.uniform(-90, 90)
        self.image = self.bug_image()

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.rotation)
        rect = rotated_image.get_rect(center=self.position)
        screen.blit(rotated_image, rect)

    def update(self, dt):
        self.position += self.velocity * dt
        self.rotation += self.rotation_speed * dt

    def bug_image(self):
        size = int(self.radius * 2.8)
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        center = pygame.Vector2(size / 2, size / 2)
        body_rect = pygame.Rect(0, 0, self.radius * 1.45, self.radius * 2.0)
        body_rect.center = center
        head = center + pygame.Vector2(0, -self.radius * 0.95)

        colors = {
            "beetle": ((58, 163, 95), (32, 94, 66), (12, 48, 34)),
            "ladybug": ((218, 58, 54), (37, 37, 37), (10, 10, 10)),
            "roach": ((153, 102, 56), (92, 58, 36), (45, 31, 24)),
        }
        body_color, detail_color, dark_color = colors[self.bug_kind]

        for side in (-1, 1):
            for y_offset in (-0.42, 0.05, 0.48):
                start = center + pygame.Vector2(
                    side * self.radius * 0.55, self.radius * y_offset
                )
                mid = start + pygame.Vector2(
                    side * self.radius * 0.62, self.radius * 0.12
                )
                end = mid + pygame.Vector2(
                    side * self.radius * 0.35, self.radius * 0.34
                )
                pygame.draw.lines(
                    surface, detail_color, False, (start, mid, end), LINE_WIDTH + 1
                )

        pygame.draw.ellipse(surface, body_color, body_rect)
        pygame.draw.ellipse(surface, dark_color, body_rect, LINE_WIDTH + 1)
        pygame.draw.circle(surface, dark_color, head, self.radius * 0.45)
        pygame.draw.line(
            surface,
            detail_color,
            center + pygame.Vector2(0, -self.radius * 0.85),
            center + pygame.Vector2(0, self.radius * 0.85),
            LINE_WIDTH,
        )

        if self.bug_kind == "ladybug":
            spots = ((-0.3, -0.35), (0.3, -0.2), (-0.25, 0.25), (0.28, 0.42))
            for x_offset, y_offset in spots:
                pygame.draw.circle(
                    surface,
                    dark_color,
                    center
                    + pygame.Vector2(self.radius * x_offset, self.radius * y_offset),
                    max(3, int(self.radius * 0.14)),
                )
        elif self.bug_kind == "beetle":
            pygame.draw.ellipse(
                surface,
                (111, 218, 132),
                pygame.Rect(
                    center.x - self.radius * 0.28,
                    center.y - self.radius * 0.55,
                    self.radius * 0.56,
                    self.radius * 1.1,
                ),
                LINE_WIDTH,
            )
        else:
            for y_offset in (-0.35, 0.0, 0.35):
                segment = pygame.Rect(
                    center.x - self.radius * 0.52,
                    center.y + self.radius * y_offset,
                    self.radius * 1.04,
                    self.radius * 0.42,
                )
                pygame.draw.arc(
                    surface,
                    detail_color,
                    segment,
                    0,
                    3.14,
                    LINE_WIDTH,
                )

        for side in (-1, 1):
            eye = head + pygame.Vector2(
                side * self.radius * 0.16, -self.radius * 0.08
            )
            pygame.draw.circle(surface, "white", eye, max(2, int(self.radius * 0.08)))
            antenna_start = head + pygame.Vector2(
                side * self.radius * 0.18, -self.radius * 0.25
            )
            antenna_end = antenna_start + pygame.Vector2(
                side * self.radius * 0.45, -self.radius * 0.42
            )
            pygame.draw.line(
                surface, detail_color, antenna_start, antenna_end, LINE_WIDTH
            )

        return surface

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
