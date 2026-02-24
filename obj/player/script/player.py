from module.behaviors import*
from obj.bullet.script.bullet import*

class PLAYER(BEHAVIORS):
    def __init__(self):
        self.size = (64, 64)
        self.color = RED 
        self.index = 0
        self.last_change = p.time.get_ticks()
        self.moving = False
        raw_images = image_load(os.path.dirname(__file__))
        self.original_image = p.transform.scale(raw_images[0], self.size)
        self.last_change = p.time.get_ticks()
        self.image = self.original_image
        self.frames = []
        for img in raw_images:
            self.frames.append(p.transform.scale(img, self.size))
        
        self.rect = self.image.get_rect(topleft=(64, 64))
        
        self.pos_x = float(self.rect.centerx)
        self.pos_y = float(self.rect.centery)
        
        self.speed = 3
        self.angle = 0

        self.max_health = 200
        self.health = self.max_health
        self.lives = 2
        self.last_regen = p.time.get_ticks()
        self.regen_speed = 3000
        self.regen_amount = 5

        self.damage = 20

        self.last_shot = 0
        self.shoot_delay = 500

        self.god_mode = False

    def reset_stats(self):
        self.max_health = 200
        self.health = min(self.health, self.max_health)
        self.damage = 20
        self.speed = 3
        self.shoot_delay = 500
        self.lives = 2
        self.regen_speed = 3000
        self.regen_amount = 5
        self.god_mode = False

    def regenerate(self):
        now = p.time.get_ticks()
        if now - self.last_regen > self.regen_speed:
            self.last_regen = now
            if self.health < self.max_health:
                self.health = min(self.health + self.regen_amount, self.max_health)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.lives -= 1
            self.health = self.max_health
        if self.lives <= 0:
            return True
        return False

    def move(self, walls):
        keys = p.key.get_pressed()
        old_x, old_y = self.pos_x, self.pos_y
        old_angle = self.angle
        
        if keys[p.K_a]: self.angle += 3
        if keys[p.K_d]: self.angle -= 3
        
        rad = math.radians(self.angle - 90)
        dist_x = 0
        dist_y = 0
        
        if keys[p.K_s]:
            dist_x = self.speed * math.cos(rad)
            dist_y = -self.speed * math.sin(rad)
        if keys[p.K_w]:
            dist_x = -self.speed * math.cos(rad)
            dist_y = self.speed * math.sin(rad)

        collision_rect = p.Rect(0, 0, 30, 30) 

        self.pos_x += dist_x
        collision_rect.center = (int(self.pos_x), int(self.pos_y))
        for wall in walls:
            if collision_rect.colliderect(wall.rect):
                self.pos_x = old_x
                break

        self.pos_y += dist_y
        collision_rect.center = (int(self.pos_x), int(self.pos_y))
        for wall in walls:
            if collision_rect.colliderect(wall.rect):
                self.pos_y = old_y
                break

        if self.pos_x != old_x or self.pos_y != old_y or self.angle != old_angle:
            self.moving = True
        else:
            self.moving = False

        self.image = p.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=(int(self.pos_x), int(self.pos_y)))

    def attack(self, bullets_list):
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
            
            new_bullet = BULLET(spawn_x, spawn_y, (dx, dy))
            bullets_list.append(new_bullet)

    def draw_ui(self):
        bar_width = 200
        bar_height = 20
        x, y = 10, 10
        hp_fill = (self.health / self.max_health) * bar_width
        
        color = (255, 215, 0) if self.god_mode else (0, 255, 0)
        
        p.draw.rect(SCREEN, (50, 50, 50), (x, y, bar_width, bar_height))
        p.draw.rect(SCREEN, color, (x, y, hp_fill, bar_height))
        p.draw.rect(SCREEN, (255, 255, 255), (x, y, bar_width, bar_height), 2)

        font = p.font.SysFont("Arial", 24, bold=True)
        text = "GOD" if self.god_mode else f"{self.lives}"
        lives_text = font.render(text, True, (255, 255, 255))
        
        SCREEN.blit(lives_text, (x + bar_width + 15, y - 2))

player = PLAYER()

