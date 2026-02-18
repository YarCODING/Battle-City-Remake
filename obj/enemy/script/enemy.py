from abc import ABC, abstractmethod
from module.behaviors import*

class ENEMY(ABC, BEHAVIORS):
    def __init__(self, x, y, frames, speed, health):
        self.frames = frames
        self.index = 0
        self.original_image = self.frames[self.index]
        self.image = self.original_image
        
        self.size = self.image.get_size() 
        
        self.rect = self.image.get_rect(center=(x, y))
        self.pos_x = float(self.rect.centerx)
        self.pos_y = float(self.rect.centery)
        
        self.speed = speed
        self.max_health = health
        self.health = self.max_health
        self.angle = 0
        self.moving = False
        self.last_change = p.time.get_ticks()

        self.max_health = 100
        self.health = self.max_health
        self.health_timer = 0

    def take_damage(self, amount):
        self.health -= amount
        self.health_timer = p.time.get_ticks()
    def draw_hp(self):
        if p.time.get_ticks() - self.health_timer < 2000:
            bar_width = self.rect.width
            hp_fill = (self.health / self.max_health) * bar_width
            p.draw.rect(SCREEN, (255, 0, 0), (self.rect.x, self.rect.y - 10, bar_width, 5))
            p.draw.rect(SCREEN, (0, 255, 0), (self.rect.x, self.rect.y - 10, hp_fill, 5))

    def update_animation(self):
        if self.moving:
            now = p.time.get_ticks()
            if now - self.last_change > 150:
                self.last_change = now
                self.index = (self.index + 1) % len(self.frames)
                self.original_image = self.frames[self.index]

    @abstractmethod
    def move(self, target_pos, walls):
        pass

    @abstractmethod
    def attack(self):
        pass

enemies = []