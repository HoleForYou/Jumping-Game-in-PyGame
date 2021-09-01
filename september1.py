# Imports
import pygame as py
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
import sys
import random

# initialisation
py.init()
vec = py.math.Vector2

# Variables
height = 450
width = 500
acc = 1
friction = -0.12
fps = 60

# Clock
frames_per_second = py.time.Clock()

# Display Code
display_surface = py.display.set_mode((width, height))
py.display.set_caption("Platformer Game")

# Classes


class player(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = py.Surface((30, 30))
        self.surf.fill((255, 102, 204))
        self.rect = self.surf.get_rect()

        self.pos = vec((10, 385))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def move(self):
        self.acc = vec(0, 0.5)

        pressed_keys = py.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.acc.x = -acc
        if pressed_keys[K_RIGHT]:
            self.acc.x = acc
        self.acc.x += self.vel.x * friction
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        if self.pos.x > width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = width

        self.rect.midbottom = self.pos

    def update(self):
        hits = py.sprite.spritecollide(p1, platforms, False)
        if p1.vel.y > 0:
            if hits:
                self.pos.y = hits[0].rect.top + 1
                self.vel.y = 0

    def jump(self):
        hits = py.sprite.spritecollide(self, platforms, False)
        if hits:
            self.vel.y = -15


class platform(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = py.Surface((random.randint(50, 100), 12))
        self.surf.fill((0, 150, 255))
        self.rect = self.surf.get_rect(center=(random.randint(
            0, width - 10), random.randint(0, height - 30)))

    def move(self):
        pass

# Randomly generating platforms on screen to make the game infiniteb


def plat_gen():
    while len(platforms) < 7:
        plat_gen_width = random.randrange(50, 500)
        p = platform()
        p.rect.center = (random.randrange(0, plat_gen_width),
                         random.randrange(-50, 0))
        platforms.add(p)
        all_sprites.add(p)


# Sprites
pt1 = platform()
p1 = player()

# Platform code
pt1.surf = py.Surface((width, 20))
pt1.surf.fill((0, 150, 255))
pt1.rect = pt1.surf.get_rect(center=(width / 2, height - 10))

# Sprite Group
all_sprites = py.sprite.Group()
all_sprites.add(pt1)
all_sprites.add(p1)

platforms = py.sprite.Group()
platforms.add(pt1)

# Random platform generating code in the beginning of the game
for x in range(random.randint(5, 6)):
    pl = platform()
    platforms.add(pl)
    all_sprites.add(pl)
    print("hello pygame")


# Game Loop
running = True
while running:
    # for getting the key presses
    for event in py.event.get():
        # For closing the game
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        # The jump feature
        if event.type == py.KEYDOWN:
            if event.key == py.K_SPACE:
                p1.jump()

    # Infinite scrolling code
    if p1.rect.top <= height / 3:
        p1.pos.y += abs(p1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(p1.vel.y)
            if plat.rect.top >= height:
                plat.kill()

    display_surface.fill((0, 0, 0))

    # generate the platforms
    plat_gen()
    p1.move()
    p1.update()
    for entity in all_sprites:
        display_surface.blit(entity.surf, entity.rect)

    py.display.update()
    frames_per_second.tick(fps)
