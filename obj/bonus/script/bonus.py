from module.behaviors import*

class BONUS(BEHAVIORS):
    def __init__(self, x, y):
        self.types = ['hp', 'lives', 'speed', 'star']
        self.type = random.choice(self.types)
        raw_images = image_load(os.path.dirname(__file__))
        if self.type == 'hp': self.image = raw_images[0]
        elif self.type == 'lives': self.image = raw_images[1]
        elif self.type == 'speed': self.image = raw_images[2]
        elif self.type == 'star': self.image = raw_images[3]
        
        self.rect = self.image.get_rect(center=(x, y))
        self.spawn_time = p.time.get_ticks()
        self.lifetime = 10000


bonuses = []