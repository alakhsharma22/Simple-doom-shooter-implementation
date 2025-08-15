import pygame
import math
from config import *

def ray_casting(player):
    rays = []
    cur_angle = player.angle - HALF_FOV
    for _ in range(NUM_RAYS):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)
        
        y_hor, dy = (int(player.y) + 1, 1) if sin_a > 0 else (int(player.y) - 1e-6, -1)
        depth_hor = (y_hor - player.y) / sin_a
        x_hor = player.x + depth_hor * cos_a
        delta_depth = dy / sin_a
        dx = delta_depth * cos_a
        for i in range(MAX_DEPTH):
            tile_x, tile_y = int(x_hor), int(y_hor)
            if not (0 <= tile_x < MAP_WIDTH and 0 <= tile_y < MAP_HEIGHT): break
            if MAP[tile_y][tile_x] == 1: break
            x_hor += dx; y_hor += dy; depth_hor += delta_depth
        
        x_vert, dx = (int(player.x) + 1, 1) if cos_a > 0 else (int(player.x) - 1e-6, -1)
        depth_vert = (x_vert - player.x) / cos_a
        y_vert = player.y + depth_vert * sin_a
        delta_depth = dx / cos_a
        dy = delta_depth * sin_a
        for i in range(MAX_DEPTH):
            tile_x, tile_y = int(x_vert), int(y_vert)
            if not (0 <= tile_x < MAP_WIDTH and 0 <= tile_y < MAP_HEIGHT): break
            if MAP[tile_y][tile_x] == 1: break
            x_vert += dx; y_vert += dy; depth_vert += delta_depth
            
        depth = min(depth_hor, depth_vert)
        depth *= math.cos(player.angle - cur_angle)
        rays.append(depth)
        cur_angle += DELTA_ANGLE
    return rays

def draw_scene(screen, rays, sprites, player, z_buffer):
    screen.fill(SKY_COLOR, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
    screen.fill(GROUND_COLOR, (0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
    
    for i, depth in enumerate(rays):
        if depth == 0: depth = 0.0001
        proj_height = min(int(SCREEN_HEIGHT / depth), SCREEN_HEIGHT * 2)
        c = max(50, 255 / (1 + depth * 0.1))
        color = (c, c, c)
        wall_rect = pygame.Rect(i * (SCREEN_WIDTH / NUM_RAYS), SCREEN_HEIGHT // 2 - proj_height // 2, (SCREEN_WIDTH / NUM_RAYS) + 1, proj_height)
        pygame.draw.rect(screen, color, wall_rect)
        z_buffer[i] = depth

    sprite_projections = []
    for sprite in sprites:
        if not sprite.is_dead:
            proj = sprite.get_sprite_projection(player)
            if proj:
                sprite_projections.append(proj)

    sprite_projections.sort(key=lambda x: x[0], reverse=True)

    for dist, image, x, y in sprite_projections:
        start_col = int(x / (SCREEN_WIDTH / NUM_RAYS))
        end_col = int((x + image.get_width()) / (SCREEN_WIDTH / NUM_RAYS))
        for col in range(start_col, end_col):
            if 0 <= col < NUM_RAYS and z_buffer[col] >= dist:
                screen.blit(image, (x, y))
                break