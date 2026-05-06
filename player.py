import pygame

from circleshape import CircleShape
from constants import (
    LINE_WIDTH,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_SHOOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
)
from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius=radius)
        self.rotation = 0
        self.cooldown = 0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90)
        center = self.position

        cheek_radius = self.radius * 0.58
        cheek_offset = self.radius * 0.42
        left_cheek = center - right * cheek_offset
        right_cheek = center + right * cheek_offset
        waist = center - forward * self.radius * 0.72
        sparkle = center + forward * self.radius * 0.82

        pygame.draw.circle(screen, (255, 177, 154), left_cheek, cheek_radius)
        pygame.draw.circle(screen, (255, 177, 154), right_cheek, cheek_radius)
        pygame.draw.circle(
            screen, (230, 126, 111), left_cheek, cheek_radius, LINE_WIDTH
        )
        pygame.draw.circle(
            screen, (230, 126, 111), right_cheek, cheek_radius, LINE_WIDTH
        )

        pygame.draw.line(
            screen,
            (255, 238, 180),
            waist - right * self.radius * 0.72,
            waist + right * self.radius * 0.72,
            LINE_WIDTH + 1,
        )
        pygame.draw.line(
            screen,
            (245, 116, 129),
            center - forward * self.radius * 0.1,
            center + forward * self.radius * 0.45,
            LINE_WIDTH,
        )
        pygame.draw.circle(
            screen, (255, 255, 255), sparkle, max(2, self.radius * 0.12)
        )

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def update(self, dt):
        self.cooldown -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        if self.cooldown > 0:
            return
        else:
            self.cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
            shot = Shot(self.position)
            shot.velocity = (
                pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
            )
