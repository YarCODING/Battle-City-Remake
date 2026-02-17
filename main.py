from imports import*
from module.texts import*

game = True
in_title_screen = True

maps_obj = create_lvl(0)
solids_obj = []
LVL = 1

def start_lvl():
    for wall in maps_obj:
        if wall.index == 1:
            wall.draw_img()
            solids_obj.append(wall)
start_lvl()

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

        for wall in maps_obj:
            if wall.index != 1:
                wall.draw_img()

        if player.rect.right < 0 or player.rect.left > SCREENSIZE[0] or \
            player.rect.bottom < 0 or player.rect.top > SCREENSIZE[1]:
                
                player.pos_x = 64.0
                player.pos_y = 64.0
                player.angle = 0
                logging.debug("Player respawned")
                
                player.rect.center = (player.pos_x, player.pos_y)

        player.move(maps_obj)
        player.draw_img()

        for b in bullets[:]:
            b.move()
            b.draw_img()
            if b.rect.right < 0 or b.rect.left > SCREENSIZE[0] or b.rect.bottom < 0 or b.rect.top > SCREENSIZE[1]:
                bullets.remove(b)
                logging.debug("Bullet - deleted (screen)")
            
            for wall in maps_obj:
                if b.rect.colliderect(wall.rect):
                    bullets.remove(b)
                    logging.debug("Bullet - deleted (wall)")
                    break
        

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
                    logging.debug("Bullet - spawned")
        now = p.time.get_ticks()
        if player.moving == True:
            if now - player.last_change > 200:
                player.last_change = now
                player.index += 1
                if player.index == 1:
                    player.original_image = p.transform.scale(
                        p.image.load("obj/player/img/tank2.png"),
                        player.size
                    )
                elif player.index == 2:
                    player.original_image = p.transform.scale(
                        p.image.load("obj/player/img/tank3.png"),
                        player.size
                    )
                elif player.index == 3:
                    player.original_image = p.transform.scale(
                        p.image.load("obj/player/img/tank4.png"),
                        player.size
                    )
                elif player.index == 4:
                    player.original_image = p.transform.scale(
                        p.image.load("obj/player/img/tank1.png"),
                        player.size
                    )
                    player.index = 0


p.quit()


