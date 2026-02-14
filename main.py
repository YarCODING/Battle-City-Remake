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
        self.rect = pygame.Rect(x, y, w, h)
        self.original_image = pygame.transform.scale(image, (w, h))
        self.image = self.original_image
        self.speed = speed

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def move(self):
        keys = pygame.key.get_pressed()

        moving = False

        if keys[pygame.K_w]:
            self.rect.y -= self.speed
            self.image = pygame.transform.rotate(self.original_image, -360)
            moving = True

        if keys[pygame.K_s]:
            self.rect.y += self.speed
            self.image = pygame.transform.rotate(self.original_image, 180)
            moving = True

        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.image = pygame.transform.rotate(self.original_image, 90)
            moving = True

        if keys[pygame.K_d]:
            self.rect.x += self.speed
            self.image = self.original_image
            self.image = pygame.transform.rotate(self.original_image, -90)
            moving = True



player = Player(300, 200, 50, 50, player_img, 3)

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

        pygame.display.update()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False

pygame.quit()
