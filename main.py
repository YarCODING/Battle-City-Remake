import math

import pygame

pygame.init()

FPS = 60
clock = pygame.time.Clock()
wind_w, wind_h = 700, 500
window = pygame.display.set_mode((wind_w, wind_h))
pygame.display.set_caption("Battle_City_Remake")


# pygame.mixer.music.load("land.ogg")
# pygame.mixer.music.set_volume(0.05)


background = pygame.image.load("images.jpg")
background = pygame.transform.scale(background, (wind_w, wind_h))
player_img = pygame.image.load("tank1.PNG")


title_font = pygame.font.SysFont("Arial", 30)
play_text = title_font.render("Play Game", True, (255, 255, 255))
close_text = title_font.render("Close Game", True, (255, 255, 255))


play_button_rect = pygame.Rect(250, 200, 200, 60)
close_button_rect = pygame.Rect(250, 300, 200, 60)


class Player:
    def __init__(self, x, y, w, h, image, speed):
        self.original_image = pygame.transform.scale(image, (w, h))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = speed
        self.angle = 0

    def draw(self):
        window.blit(self.image, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.angle += 3
        if keys[pygame.K_d]:
            self.angle -= 3
        if keys[pygame.K_s]:
            self.rect.x += self.speed * math.cos(math.radians(self.angle - 90))
            self.rect.y -= self.speed * math.sin(math.radians(self.angle - 90))
        if keys[pygame.K_w]:
            self.rect.x -= self.speed * math.cos(math.radians(self.angle - 90))
            self.rect.y += self.speed * math.sin(math.radians(self.angle - 90))
        center = self.rect.center
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=center)



player = Player(300, 200, 50, 50, player_img, 3)


class Bullet:
    def __init__(self, x, y, direction, speed=7, size=6, color=(255, 0, 0)):
        self.rect = pygame.Rect(0, 0, size, size)
        self.rect.center = (x, y)
        self.dir = direction
        self.speed = speed
        self.color = color

    def update(self):
        self.rect.x += self.dir[0] * self.speed
        self.rect.y += self.dir[1] * self.speed

    def draw(self):
        pygame.draw.rect(window, self.color, self.rect)


bullets = []

game = True
in_title_screen = True

while game:
    if in_title_screen:
        window.blit(background, (0, 0))
        window.blit(title_font.render("Battle_City_Remake", True, (0, 0, 0)), (300, 130))

        pygame.draw.rect(window, (0, 255, 0), play_button_rect)
        pygame.draw.rect(window, (255, 0, 0), close_button_rect)

        window.blit(play_text, (play_button_rect.x + 30, play_button_rect.y + 10))
        window.blit(close_text, (close_button_rect.x + 30, close_button_rect.y + 10))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    in_title_screen = False
                    # pygame.mixer.music.play(-1)

                if close_button_rect.collidepoint(event.pos):
                    game = False

    else:
        window.blit(background, (0, 0))

        player.move()
        player.draw()

        for b in bullets[:]:
            b.update()
            b.draw()
            if b.rect.right < 0 or b.rect.left > wind_w or b.rect.bottom < 0 or b.rect.top > wind_h:
                bullets.remove(b)

        pygame.display.update()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    px, py = player.rect.center
                    rad = math.radians(player.angle - 90)
                    dx = -math.cos(rad)
                    dy = math.sin(rad)
                    offset = max(player.rect.width, player.rect.height) / 2 + 8
                    spawn_x = px + dx * offset
                    spawn_y = py + dy * offset
                    bullets.append(Bullet(spawn_x, spawn_y, (dx, dy)))

pygame.quit()
