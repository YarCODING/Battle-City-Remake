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

        for enemy in enemies:
            enemy.move()
            enemy.draw_img()
            enemy.draw_hp()
            enemy.attack(enemy_bullets)

        player.move(maps_obj)
        player.draw_img()
        player.draw_ui()

        for b in bullets[:]:
            b.move()
            b.draw_img()
            if b.rect.right < 0 or b.rect.left > SCREENSIZE[0] or b.rect.bottom < 0 or b.rect.top > SCREENSIZE[1]:
                bullets.remove(b)
                logging.debug("Bullet - deleted (screen)")
            
            for wall in maps_obj[:]:
                if b.rect.colliderect(wall.rect):
                    if not wall.indestructible:
                        wall.health -= 10
                        if wall.health <= 0: maps_obj.remove(wall)
                    if b in bullets: bullets.remove(b)
                    break

            for enemy in enemies[:]:
                if b.rect.colliderect(enemy.rect):
                    enemy.take_damage(20)
                    if b in bullets: bullets.remove(b)
                    if enemy.health <= 0: enemies.remove(enemy)
                    break
        for eb in enemy_bullets[:]:
            eb.move()
            eb.draw_img()
            for wall in maps_obj[:]:
                if eb.rect.colliderect(wall.rect):
                    if eb in enemy_bullets: enemy_bullets.remove(eb)
                    break
            if eb.rect.right < 0 or eb.rect.left > SCREENSIZE[0] or \
            eb.rect.bottom < 0 or eb.rect.top > SCREENSIZE[1]:
                enemy_bullets.remove(eb)

            if eb.rect.colliderect(player.rect):
                enemy_bullets.remove(eb)
                player.take_damage(20)
                


        p.display.update()
        clock.tick(FPS)

        for event in p.event.get():
            if event.type == p.QUIT:
                game = False
            if event.type == p.KEYDOWN:
                if event.key == p.K_ESCAPE:
                    in_title_screen = True
                if event.key == p.K_SPACE:
                    player.attack(bullets)


        now = p.time.get_ticks()
        if player.moving:
            if now - player.last_change > 300:
                player.last_change = now
                player.index = (player.index + 1) % len(player.frames)
                
                player.original_image = player.frames[player.index]
                player.image = p.transform.rotate(player.original_image, player.angle)


p.quit()






