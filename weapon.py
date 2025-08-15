from config import SCREEN_WIDTH, SCREEN_HEIGHT

class Weapon:
    def __init__(self, pistol_images, shoot_sound):
        self.images = pistol_images
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - self.rect.height // 2 + 50)
        self.shoot_sound = shoot_sound
        self.shooting = False
        self.animation_frame = 0
        self.animation_speed = 3
        self.frame_counter = 0
        self.ammo = 30

    def shoot(self):
        if not self.shooting and self.ammo > 0:
            self.shooting = True
            self.animation_frame = 1
            self.shoot_sound.play()
            self.ammo -= 1
            return True
        return False

    def update(self):
        if self.shooting:
            self.frame_counter += 1
            if self.frame_counter >= self.animation_speed:
                self.frame_counter = 0
                self.animation_frame += 1
                if self.animation_frame >= len(self.images):
                    self.animation_frame = 0
                    self.shooting = False
            self.image = self.images[self.animation_frame]
        else:
            self.image = self.images[0]

    def draw(self, screen):
        screen.blit(self.image, self.rect)