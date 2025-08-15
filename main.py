import pygame
import random
import math

from config import *
from player import Player
from sprite import Sprite
from weapon import Weapon
from drawing import ray_casting, draw_scene

def create_placeholder_target():
    target = pygame.Surface((64, 64), pygame.SRCALPHA)
    pygame.draw.circle(target, RED, (32, 32), 30)
    pygame.draw.circle(target, WHITE, (32, 32), 20)
    pygame.draw.circle(target, RED, (32, 32), 10)
    return target

def create_placeholder_pistol():
    pistol_base = pygame.Surface((400, 300), pygame.SRCALPHA)
    pygame.draw.rect(pistol_base, (50, 50, 50), (160, 120, 60, 150), border_radius=5)
    pygame.draw.rect(pistol_base, (80, 80, 80), (120, 80, 200, 70), border_radius=3)
    pygame.draw.rect(pistol_base, (100, 100, 100), (320, 95, 80, 40))
    pistol_frames = [pistol_base]
    for i in range(1, 4):
        frame = pistol_base.copy()
        flash_size = 50 - i * 7
        flash_center = (400, 115)
        pygame.draw.circle(frame, (255, 255, 0), flash_center, flash_size)
        pygame.draw.circle(frame, (255, 165, 0), flash_center, flash_size // 2)
        pistol_frames.append(frame)
    return pistol_frames

class DummySound:
    def play(self): pass

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("DOOM Hen Shooter")
    clock = pygame.time.Clock()
    
    font = pygame.font.Font(None, 50)
    large_font = pygame.font.Font(None, 100)
    
    score = 0
    game_over = False
    start_time = pygame.time.get_ticks()

    target_img = create_placeholder_target()
    pistol_imgs = create_placeholder_pistol()
    shoot_sound = DummySound()
    
    player = Player(1.5, 1.5, math.pi / 4)
    weapon = Weapon(pistol_imgs, shoot_sound)
    sprites = [Sprite(random.uniform(1.5, MAP_WIDTH - 1.5), random.uniform(1.5, MAP_HEIGHT - 1.5), target_img) for _ in range(20) if MAP[int(random.uniform(1.5, MAP_HEIGHT-1.5))][int(random.uniform(1.5, MAP_WIDTH-1.5))] == 0]
    z_buffer = [MAX_DEPTH] * NUM_RAYS

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            
            if not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if weapon.shoot():
                        for sprite in sorted([s for s in sprites if not s.is_dead], key=lambda s: (p := s.get_sprite_projection(player)) is not None and p[0]):
                            proj = sprite.get_sprite_projection(player)
                            if proj:
                                dist, img, x, y = proj
                                if x < SCREEN_WIDTH // 2 < x + img.get_width() and y < SCREEN_HEIGHT // 2 < y + img.get_height():
                                    sprite.is_dead = True
                                    score += 10
                                    break
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    main() 
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    running = False

        if not game_over:
            pygame.mouse.set_visible(False)
            player.movement()
            weapon.update()
            for sprite in sprites:
                sprite.update()
            
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
            remaining_time = max(0, GAME_DURATION_SECONDS - elapsed_time)
            if remaining_time == 0:
                game_over = True
                pygame.mouse.set_visible(True)

        screen.fill(BLACK)
        rays = ray_casting(player)
        draw_scene(screen, rays, sprites, player, z_buffer)
        weapon.draw(screen)

        if not game_over:
            pygame.draw.line(screen, RED, (SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2), (SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2), 2)
            pygame.draw.line(screen, RED, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10), 2)
            
            ammo_text = font.render(f'AMMO: {weapon.ammo}', True, WHITE)
            screen.blit(ammo_text, (50, SCREEN_HEIGHT - 70))
            score_text = font.render(f'SCORE: {score}', True, WHITE)
            screen.blit(score_text, (SCREEN_WIDTH - 250, SCREEN_HEIGHT - 70))
            
            minutes = int(remaining_time) // 60
            seconds = int(remaining_time) % 60
            timer_text = font.render(f'TIME: {minutes:02}:{seconds:02}', True, WHITE)
            screen.blit(timer_text, (SCREEN_WIDTH // 2 - 80, 20))
        else:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill(UI_BG_COLOR)
            screen.blit(overlay, (0, 0))

            game_over_text = large_font.render('TIME UP!', True, RED)
            final_score_text = font.render(f'Final Score: {score}', True, WHITE)
            ammo_saved_text = font.render(f'Ammo Remaining: {weapon.ammo}', True, WHITE)
            restart_text = font.render('Press [R] to Restart or [Q] to Quit', True, WHITE)
            
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 150))
            screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))
            screen.blit(ammo_saved_text, (SCREEN_WIDTH // 2 - ammo_saved_text.get_width() // 2, SCREEN_HEIGHT // 2 + 30))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()