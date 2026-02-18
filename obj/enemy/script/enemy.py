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