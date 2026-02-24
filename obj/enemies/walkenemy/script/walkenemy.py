from obj.enemy.script.enemy import*
from obj.bullet.script.bullet import*
from obj.bullet.script.bullet_enemy import*

class WALK_ENEMY_V(ENEMY):
    def __init__(self, x, y, frames, speed, y2):
        super().__init__(x, y, frames, speed, health=100)
        
        self.y1 = float(y)
        self.y2 = float(y2)
        
        self.direction = 'down'
        
        self.frames_down = [p.transform.flip(img, False, True) for img in frames]
        self.frames_up = frames

        self.last_shot = 0
        self.shoot_delay = 2000

    def move(self):
        if self.pos_y >= self.y2:
            self.direction = 'up'
            self.frames = self.frames_up
        elif self.pos_y <= self.y1:
            self.direction = 'down'
            self.frames = self.frames_down

        if self.direction == 'down':
            self.angle = 180
            self.pos_y += self.speed
        else:
            self.angle = 0
            self.pos_y -= self.speed

        self.moving = True
        self.update_animation()

        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=(int(self.pos_x), int(self.pos_y)))
    
    def attack(self, enemy_bullets):
        now = p.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            
            px, py = self.rect.center
            
            rad = math.radians(self.angle - 90)
            dx = -math.cos(rad)
            dy = math.sin(rad)
            
            offset = max(self.rect.width, self.rect.height) / 2 + 10
            spawn_x = px + dx * offset
            spawn_y = py + dy * offset
            
            new_enemy_bullet = BULLET_ENEMY(spawn_x, spawn_y, (dx, dy))
            enemy_bullets.append(new_enemy_bullet)

class WALK_ENEMY_H(ENEMY):
    def __init__(self, x, y, frames, speed, x2):
        super().__init__(x, y, frames, speed, health=100)
        self.x1 = float(x)
        self.x2 = float(x2)
        self.direction = 'right'
        
        self.frames_right = frames
        self.frames_left = [p.transform.flip(img, True, False) for img in frames]
        self.frames = self.frames_right

        self.last_shot = 0
        self.shoot_delay = 2000

        self.max_health = 100
        self.health = self.max_health

    def move(self):
        if self.pos_x >= self.x2:
            self.direction = 'left'
            self.frames = self.frames_left
        elif self.pos_x <= self.x1:
            self.direction = 'right'
            self.frames = self.frames_right

        if self.direction == 'right':
            self.angle = -90
            self.pos_x += self.speed
        else:
            self.angle = 90
            self.pos_x -= self.speed

        self.moving = True
        self.update_animation()

        self.image = p.transform.rotate(self.frames[self.index], self.angle)
        self.rect = self.image.get_rect(center=(int(self.pos_x), int(self.pos_y)))
    
    def attack(self, enemy_bullets):
        now = p.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            
            px, py = self.rect.center
            
            rad = math.radians(self.angle - 90)
            dx = -math.cos(rad)
            dy = math.sin(rad)
            
            offset = max(self.rect.width, self.rect.height) / 2 + 10
            spawn_x = px + dx * offset
            spawn_y = py + dy * offset
            
            new_enemy_bullet = BULLET_ENEMY(spawn_x, spawn_y, (dx, dy))
            enemy_bullets.append(new_enemy_bullet)

            
w_enemy_raw = image_load("obj/enemy/vertical_img/")
W_RESOURCES = [p.transform.scale(img, (64, 64)) for img in w_enemy_raw]