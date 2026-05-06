import sys

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import (
    ASTEROID_MIN_RADIUS,
    PLAYER_RADIUS,
    SCORE_COLOR,
    SCORE_FONT_SIZE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from logger import log_event, log_state
from player import Player
from shot import Shot


def main():
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    dt = 0

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Bug Smashers")
    score_font = pygame.font.Font(None, SCORE_FONT_SIZE)
    score = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)

    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2

    player = Player(x, y, PLAYER_RADIUS)
    asteroid_field = AsteroidField()

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")
        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()
                return

            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    score += int(ASTEROID_MIN_RADIUS * 4 / asteroid.radius) * 100
                    shot.kill()
                    asteroid.split()
                    break

        for sprite in drawable:
            sprite.draw(screen)

        score_surface = score_font.render(f"Score: {score}", True, SCORE_COLOR)
        screen.blit(score_surface, (20, 18))

        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
