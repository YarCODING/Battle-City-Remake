from imports import*
from module.texts import*

game = True
menu_screen = 'start'

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
    if menu_screen == 'start':
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
                    menu_screen = None
                    # p.mixer.music.play(-1)

                if close_button_rect.collidepoint(event.pos):
                    game = False

    elif menu_screen == 'pause':
        SCREEN.blit(background, (0, 0))
        SCREEN.blit(title_font.render("Pause", True, (0, 0, 0)), (320, 130))

        p.draw.rect(SCREEN, (0, 255, 0), play_button_rect)
        p.draw.rect(SCREEN, (255, 0, 0), close_button_rect)

        SCREEN.blit(continue_text, (play_button_rect.x + 30, play_button_rect.y + 10))
        SCREEN.blit(close_text, (close_button_rect.x + 30, close_button_rect.y + 10))

        p.display.update()
        
        for event in p.event.get():
            if event.type == p.QUIT:
                game = False

            if event.type == p.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    menu_screen = None

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

        now = p.time.get_ticks()
        if enemy_spawns and now - last_spawn_time > spawn_delay:
            last_spawn_time = now
            
            spawn = enemy_spawns.pop(0) 
            
            if spawn["type"] == 3:
                enemies.append(WALK_ENEMY_V(spawn["x"], spawn["y"], W_RESOURCES, speed=2, y2=spawn["y"]+300))
            elif spawn["type"] == 4:
                new_h_enemy = WALK_ENEMY_H(spawn["x"], spawn["y"], W_RESOURCES, speed=2, x2=spawn["x"] + 232)
                enemies.append(new_h_enemy)

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
                    explosions.append(EXPLOSION(b.x, b.y, EXPLOSION_FRAMES))
                    if b in bullets: bullets.remove(b)
                    break

            for enemy in enemies[:]:
                if b.rect.colliderect(enemy.rect):
                    enemy.take_damage(20)
                    if b in bullets:
                        explosions.append(EXPLOSION(enemy.pos_x, enemy.pos_y, EXPLOSION_FRAMES))
                        bullets.remove(b)
                    if enemy.health <= 0: 
                        explosions.append(EXPLOSION(enemy.pos_x, enemy.pos_y, EXPLOSION_FRAMES))
                        enemies.remove(enemy)
                    break
        for eb in enemy_bullets[:]:
            eb.move()
            eb.draw_img()
            for wall in maps_obj[:]:
                if eb.rect.colliderect(wall.rect):
                    if eb in enemy_bullets:
                        explosions.append(EXPLOSION(eb.x, eb.y, EXPLOSION_FRAMES))
                        enemy_bullets.remove(eb)
                    break
            if eb.rect.right < 0 or eb.rect.left > SCREENSIZE[0] or \
            eb.rect.bottom < 0 or eb.rect.top > SCREENSIZE[1]:
                enemy_bullets.remove(eb)

            if eb.rect.colliderect(player.rect):
                explosions.append(EXPLOSION(player.pos_x, player.pos_y, EXPLOSION_FRAMES))
                enemy_bullets.remove(eb)
                player.take_damage(20)
        
        for exp in explosions[:]:
            exp.update()
            if not exp.alive:
                explosions.remove(exp)
        for exp in explosions:
            exp.draw(SCREEN)
                
        p.display.update()
        clock.tick(FPS)

        for event in p.event.get():
            if event.type == p.QUIT:
                game = False
            if event.type == p.KEYDOWN:
                if event.key == p.K_ESCAPE:
                    menu_screen = 'pause'
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






