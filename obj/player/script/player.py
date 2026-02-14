from module.behaviors import*

class PLAYER(BEHAVIORS):
    def __init__(self):
        self.size = (64, 64)
        self.color = RED 
        
        raw_images = image_load(os.path.dirname(__file__))
        self.original_image = p.transform.scale(raw_images[0], self.size)
        self.image = self.original_image
        
        self.rect = self.image.get_rect(topleft=(64, 64))
        
        self.pos_x = float(self.rect.centerx)
        self.pos_y = float(self.rect.centery)
        
        self.speed = 3
        self.angle = 0

    def move(self):
        keys = p.key.get_pressed()
        
        if keys[p.K_a]:
            self.angle += 3
        if keys[p.K_d]:
            self.angle -= 3
            
        # 2. Движение
        rad = math.radians(self.angle - 90)
        if keys[p.K_s]:
            self.pos_x += self.speed * math.cos(rad)
            self.pos_y -= self.speed * math.sin(rad)
        if keys[p.K_w]:
            self.pos_x -= self.speed * math.cos(rad)
            self.pos_y += self.speed * math.sin(rad)
            
        self.image = p.transform.rotate(self.original_image, self.angle)
        
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

player = PLAYER()