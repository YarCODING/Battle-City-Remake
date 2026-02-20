from module.behaviors import*

exp_raw = image_load(os.path.dirname(__file__))
EXPLOSION_FRAMES = [p.transform.scale(img, (64, 64)) for img in exp_raw]

class EXPLOSION(BEHAVIORS):
    def __init__(self, x, y, frames):
        super().__init__()
        self.frames = frames
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        
        self.last_update = p.time.get_ticks()
        self.frame_rate = 60
        self.alive = True

    def update(self):
        now = p.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.index += 1
            
            if self.index >= len(self.frames):
                self.alive = False
            else:
                self.image = self.frames[self.index]

    def draw(self, screen):
        if self.alive:
            screen.blit(self.image, self.rect)

explosions = []