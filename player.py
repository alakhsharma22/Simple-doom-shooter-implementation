import pygame
import math
from config import PLAYER_SPEED, PLAYER_ROT_SPEED, MAP

class Player:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        
        dx, dy = 0, 0
        speed = PLAYER_SPEED
        
        if keys[pygame.K_w]:
            dx += speed * cos_a
            dy += speed * sin_a
        if keys[pygame.K_s]:
            dx -= speed * cos_a
            dy -= speed * sin_a
        if keys[pygame.K_a]: 
            dx += speed * sin_a
            dy -= speed * cos_a
        if keys[pygame.K_d]: 
            dx -= speed * sin_a
            dy += speed * cos_a

        self.check_wall_collision(dx, dy)

        if keys[pygame.K_LEFT]:
            self.angle -= PLAYER_ROT_SPEED
        if keys[pygame.K_RIGHT]:
            self.angle += PLAYER_ROT_SPEED
        self.angle %= (2 * math.pi)

    def check_wall_collision(self, dx, dy):
        buffer = 0.2
        if MAP[int(self.y)][int(self.x + dx + (buffer if dx > 0 else -buffer))] == 0:
            self.x += dx
        if MAP[int(self.y + dy + (buffer if dy > 0 else -buffer))][int(self.x)] == 0:
            self.y += dy