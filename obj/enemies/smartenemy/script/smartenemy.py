from obj.enemy.script.enemy import*
from obj.bullet.script.bullet import*
from obj.bullet.script.bullet_enemy import*
from collections import deque

class SMART_ENEMY(ENEMY):
    def __init__(self, x, y, frames, speed):
        super().__init__(x, y, frames, speed, health=150)
        self.shoot_delay = 1500
        self.last_shot = 0
        self.path = []
        self.last_path_update = 0

    def find_path(self, target_pos, walls):
        now = p.time.get_ticks()
        if now - self.last_path_update < 500 and self.path:
            return self.path
        
        self.last_path_update = now
        start_grid = (int(self.pos_x // 32), int(self.pos_y // 32))
        end_grid = (int(target_pos[0] // 32), int(target_pos[1] // 32))
        
        queue = deque([start_grid])
        came_from = {start_grid: None}
        
        blocked_tiles = {(int(w.rect.x // 32), int(w.rect.y // 32)) for w in walls if w.index == 0}

        while queue:
            current = queue.popleft()
            if current == end_grid: break
            
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                next_node = (current[0] + dx, current[1] + dy)
                if 0 <= next_node[0] < SCREENSIZE[0]//32 and 0 <= next_node[1] < SCREENSIZE[1]//32:
                    if next_node not in blocked_tiles and next_node not in came_from:
                        queue.append(next_node)
                        came_from[next_node] = current

        if end_grid not in came_from: return None
        
        path = []
        curr = end_grid
        while curr != start_grid:
            path.append(curr)
            curr = came_from[curr]
        path.reverse()
        self.path = path
        return path

    def move(self, player_pos, walls):
        path = self.find_path(player_pos, walls)
        if not path: return

        target_grid = path[0]
        target_x = target_grid[0] * 32 + 16
        target_y = target_grid[1] * 32 + 16

        old_pos = (self.pos_x, self.pos_y)

        if abs(target_x - self.pos_x) > self.speed:
            if target_x > self.pos_x:
                self.angle = 270
                self.pos_x += self.speed
            else:
                self.angle = 90
                self.pos_x -= self.speed
        elif abs(target_y - self.pos_y) > self.speed:
            if target_y > self.pos_y:
                self.angle = 180
                self.pos_y += self.speed
            else:
                self.angle = 0
                self.pos_y -= self.speed
        else:
            if self.path: self.path.pop(0)

        self.rect.center = (int(self.pos_x), int(self.pos_y))
        
        for w in walls:
            if w.index == 1 and self.rect.colliderect(w.rect):
                self.pos_x, self.pos_y = old_pos
                self.rect.center = (int(self.pos_x), int(self.pos_y))
                self.path = []
                break

        self.moving = True
        self.update_animation()
        self.image = p.transform.rotate(self.frames[self.index], self.angle)

    def can_see_player(self, player_rect, walls):
        dist_x = player_rect.centerx - self.pos_x
        dist_y = player_rect.centery - self.pos_y
        
        visible = False
        if self.angle == 0 and dist_y < 0 and abs(dist_x) < 20: visible = True
        elif self.angle == 180 and dist_y > 0 and abs(dist_x) < 20: visible = True
        elif self.angle == 90 and dist_x < 0 and abs(dist_y) < 20: visible = True
        elif self.angle == 270 and dist_x > 0 and abs(dist_y) < 20: visible = True
        
        if not visible: return False

        for wall in walls:
            if wall.index == 1:
                if wall.rect.clipline(self.rect.center, player_rect.center):
                    return False
        return True

    def attack(self, enemy_bullets, player_rect, walls):
        now = p.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            if self.can_see_player(player_rect, walls):
                self.last_shot = now
                rad = math.radians(self.angle + 90)
                dx = math.cos(rad)
                dy = -math.sin(rad)
                new_bullet = BULLET_ENEMY(self.pos_x, self.pos_y, (dx, dy))
                enemy_bullets.append(new_bullet)


s_enemy_raw = image_load("obj/enemies/smartenemy/img/")
S_RESOURCES = [p.transform.scale(img, (64, 64)) for img in s_enemy_raw]