from imports import*
from module.texts import*


bullets = []

game = True
in_title_screen = True

while game:
    if in_title_screen:
        SCREEN.blit(background, (0, 0))
        SCREEN.blit(title_font.render("Battle_City_Remake", True, (0, 0, 0)), (240, 130))

        p.draw.rect(SCREEN, (0, 255, 0), play_button_rect)
        p.draw.rect(SCREEN, (255, 0, 0), close_button_rect)

        SCREEN.blit(play_text, (play_button_rect.x + 30, play_button_rect.y + 10))
        SCREEN.blit(close_text, (close_button_rect.x + 30, close_button_rect.y + 10))

        p.display.update()

        for event in p.event.get():
            if event.type == p.QUIT:
                game = False

            if event.type == p.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    in_title_screen = False
                    # p.mixer.music.play(-1)

                if close_button_rect.collidepoint(event.pos):
                    game = False

    else:
        SCREEN.blit(background, (0, 0))

        player.move()
        player.draw_img()

        for b in bullets[:]:
            b.move()
            b.draw_rect()
            if b.rect.right < 0 or b.rect.left > SCREENSIZE[0] or b.rect.bottom < 0 or b.rect.top > SCREENSIZE[1]:
                bullets.remove(b)

        p.display.update()
        clock.tick(FPS)

        for event in p.event.get():
            if event.type == p.QUIT:
                game = False
            if event.type == p.KEYDOWN:
                if event.key == p.K_ESCAPE:
                    in_title_screen = True
                if event.key == p.K_SPACE:
                    px, py = player.rect.center
                    rad = math.radians(player.angle - 90)
                    dx = -math.cos(rad)
                    dy = math.sin(rad)
                    offset = max(player.rect.width, player.rect.height) / 2 + 8
                    spawn_x = px + dx * offset
                    spawn_y = py + dy * offset
                    bullets.append(BULLET(spawn_x, spawn_y, (dx, dy)))

p.quit()
