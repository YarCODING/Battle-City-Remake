from abc import ABC, abstractmethod
from module.behaviors import*

class ENEMY(ABC, BEHAVIORS):
    def __init__(self, x, y, size, speed, health):
        self.size = size
        self.max_health = health
        self.health = self.max_health
        self.speed = speed
        self.angle = 0
        self.moving = False
        self.index = 0
        self.last_change = p.time.get_ticks()

        raw_images = image_load(os.path.dirname(__file__))
        self.frames = [p.transform.scale(img, self.size) for img in raw_images]
        self.original_image = self.frames[0]
        self.image = self.original_image
        
        self.rect = self.image.get_rect(center=(x, y))
        self.pos_x = float(self.rect.centerx)
        self.pos_y = float(self.rect.centery)

    @abstractmethod
    def move(self, target_pos, walls):
        pass

    @abstractmethod
    def attack(self):
        pass