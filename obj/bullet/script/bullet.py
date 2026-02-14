from module.behaviors import*

class BULLET(BEHAVIORS):
    def __init__(self, x, y, direction):
        self.size = (8, 8)
        self.color = RED
        self.x = float(x)
        self.y = float(y)
        self.rect = p.Rect(int(self.x), int(self.y), self.size[0], self.size[1])
        
        self.dir = direction
        self.speed = 10

    def move(self):
        self.x += self.dir[0] * self.speed
        self.y += self.dir[1] * self.speed
        
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

bullets = []