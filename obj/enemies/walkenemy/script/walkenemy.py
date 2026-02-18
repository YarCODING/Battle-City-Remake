from obj.enemy.script.enemy import*

class WALK_ENEMY(ENEMY):
    def __init__(self, x, y, frames, speed, y2):
        super().__init__(x, y, frames, speed, health=100)
        
        self.y1 = float(y)
        self.y2 = float(y2)
        
        self.direction = 'down'
        
        self.frames_down = [p.transform.flip(img, False, True) for img in frames]
        self.frames_up = frames

    def move(self):
        if self.pos_y >= self.y2:
            self.direction = 'up'
            self.frames = self.frames_up
        elif self.pos_y <= self.y1:
            self.direction = 'down'
            self.frames = self.frames_down

        if self.direction == 'down':
            self.pos_y += self.speed
        else:
            self.pos_y -= self.speed

        self.moving = True
        self.update_animation()

        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=(int(self.pos_x), int(self.pos_y)))
    
    def attack(self):
        pass

w_enemy_raw = image_load("obj/enemy/vertical_img/")
W_RESOURCES = [p.transform.scale(img, (64, 64)) for img in w_enemy_raw]

enemies.append(WALK_ENEMY(400, 80, W_RESOURCES, speed=2, y2=400))