import math
import os
import random

import pygame


class Obstacle():
    def __init__(self, x, width):
        self.x = x
        self.width = width
        self.y_upper = 0
        self.upper_height = random.randint(200, 300)
        self.clearance = random.randint(200, 250)
        self.y_lower = self.upper_height + self.clearance
        self.lower_height = height - self.y_lower
        self.color = (160, 140, 190)
        self.shape_upper = pygame.Rect(self.x, self.y_upper, self.width, self.upper_height)
        self.shape_lower = pygame.Rect(self.x, self.y_lower, self.width, self.lower_height)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.shape_upper, 0)
        pygame.draw.rect(screen, self.color, self.shape_lower, 0)

    def movement(self, v):
        self.x -= v
        self.shape_upper = pygame.Rect(self.x, self.y_upper, self.width, self.upper_height)
        self.shape_lower = pygame.Rect(self.x, self.y_lower, self.width, self.lower_height)

    def collision(self, player):
        if self.shape_upper.colliderect(player) or self.shape_lower.colliderect(player):
            return True
        else:
            return False


class FlyingObject():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = 50
        self.width = 50
        self.shape = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image = pygame.image.load(os.path.join('owl_small.jpeg'))

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def movement(self, v):
        self.y += v
        self.shape = pygame.Rect(self.x, self.y, self.width, self.height)


def on_screen_sign(text, size, y=400):
    my_font = pygame.font.SysFont("Arial", size)
    go_render = my_font.render(text, 1, (255, 100, 100))
    x = (width - go_render.get_rect().width) / 2
    screen.blit(go_render, (x, y))


pygame.init()
width = 800
height = 700
screen = pygame.display.set_mode((width, height))

what_shows = 'menu'

obstacles = []
for i in range(21):
    obstacles.append(Obstacle(i * width / 20, width / 20))

player = FlyingObject(250, 380)
points = 0
dy = 0
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        dy = -0.1
    if keys[pygame.K_DOWN]:
        dy = 0.1
    if keys[pygame.K_SPACE]:
        if what_shows != 'in_game':
            player = FlyingObject(250, 330)
            points = 0
            dy = 0
            what_shows = 'in_game'

    screen.fill((0, 0, 0))

    if what_shows == 'menu':
        logo = pygame.image.load(os.path.join('owl.gif'))
        screen.blit(logo, (325, 150))
        on_screen_sign("Hit space to start", 40)
    elif what_shows == 'in_game':
        for p in obstacles:
            p.movement(0.5)
            p.draw()
            if p.collision(player.shape):
                what_shows = 'loose_screen'
        for p in obstacles:
            if p.x <= -p.width:
                obstacles.remove(p)
                obstacles.append(Obstacle(width, width / 20))
                points += math.fabs(dy)
        player.draw()
        player.movement(dy)
    elif what_shows == 'loose_screen':
        logo = pygame.image.load(os.path.join('owl.gif'))
        screen.blit(logo, (325, 150))
        on_screen_sign("Owl is dead as doornail,", 30)
        on_screen_sign("but before it met its gruesome death, it managed to get:", 30, 450)
        on_screen_sign(f"{points:.1f} points.", 30, 500)
        on_screen_sign("Hit space to play again!", 40, 550)

    pygame.display.update()

pygame.quit()
quit()
