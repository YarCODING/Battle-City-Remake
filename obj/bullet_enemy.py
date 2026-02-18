from module.behaviors import*

class BULLET_ENEMY(BEHAVIORS):
    def __init__(self, x, y, direction):
        self.size = (8, 21)
        self.color = RED
        self.x = float(x)
        self.y = float(y)
        
        raw_images = image_load(os.path.dirname(__file__))
        self.original_image = p.transform.scale(raw_images[0], self.size)
        
        angle_rad = math.atan2(-direction[1], direction[0])
        angle_deg = math.degrees(angle_rad) - 90
        
        self.image = p.transform.rotate(self.original_image, angle_deg)
        
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        
        self.dir = direction
        self.speed = 7

    def move(self):
        self.x += self.dir[0] * self.speed
        self.y += self.dir[1] * self.speed
        
        self.rect.center = (int(self.x), int(self.y))


enemy_bullets = []