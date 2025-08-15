import pygame
import math
import random
from config import MAP, SCREEN_WIDTH, SCREEN_HEIGHT, HALF_FOV

class Sprite:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.is_dead = False
        self.speed = 0.02
        self.angle = random.uniform(0, 2 * math.pi)

    def update(self):
        if self.is_dead:
            return
        
        dx = self.speed * math.cos(self.angle)
        dy = self.speed * math.sin(self.angle)
        
        next_x = self.x + dx
        next_y = self.y + dy

        if MAP[int(self.y)][int(next_x)] == 1 or MAP[int(next_y)][int(self.x)] == 1:
            self.angle = random.uniform(0, 2 * math.pi)
        else:
            self.x = next_x
            self.y = next_y

    def get_sprite_projection(self, player):
        dx = self.x - player.x
        dy = self.y - player.y
        distance = math.sqrt(dx**2 + dy**2)
        theta = math.atan2(dy, dx)
        gamma = theta - player.angle
        
        if gamma > math.pi: gamma -= 2 * math.pi
        if gamma < -math.pi: gamma += 2 * math.pi
        
        if abs(gamma) > HALF_FOV + 0.1:
            return None

        screen_x = SCREEN_WIDTH // 2 + math.tan(gamma) * (SCREEN_WIDTH // 2) / math.tan(HALF_FOV)
        
        if distance == 0: distance = 0.0001
        proj_height = min(int(SCREEN_HEIGHT / (distance * math.cos(gamma))), SCREEN_HEIGHT * 2)
        
        half_proj_height = proj_height // 2
        sprite_image = pygame.transform.scale(self.image, (proj_height, proj_height))
        
        return (distance, sprite_image, screen_x - half_proj_height, SCREEN_HEIGHT // 2 - half_proj_height)