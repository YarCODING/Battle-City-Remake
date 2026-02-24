from imports import*
from module.texts import*

game = True

solids_obj = []
lvl = 1

level_started = False

def start_lvl():
    global maps_obj, solids_obj, enemies, enemy_spawns, bullets, enemy_bullets, lvl, last_spawn_time, level_started

    level_started = False
    
    solids_obj.clear()
    enemies.clear()
    enemy_spawns.clear()
    bullets.clear()
    enemy_bullets.clear()
    maps_obj.clear( )
    maps_obj = create_lvl(lvl - 1, enemy_spawns)
    
    last_spawn_time = p.time.get_ticks()

    for wall in maps_obj:
        solids_obj.append(wall)

start_lvl()

while game:
    if menu_screen == 'start':
        SCREEN.blit(background, (0, 0))
        SCREEN.blit(title_font.render("Battle City Remake", True, (0, 0, 0)), (240, 130))

        p.draw.rect(SCREEN, (0, 255, 0), play_button_rect)
        p.draw.rect(SCREEN, (255, 0, 0), close_button_rect)

        SCREEN.blit(play_text, (play_button_rect.x + 30, play_button_rect.y + 10))
        SCREEN.blit(close_text, (close_button_rect.x + 30, close_button_rect.y + 10))
        
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
        
        for event in p.event.get():
            if event.type == p.QUIT:
                game = False

            if event.type == p.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    menu_screen = None

                if close_button_rect.collidepoint(event.pos):
                    game = False
    
    elif menu_screen == 'win':
        SCREEN.blit(background, (0, 0))
        SCREEN.blit(medal, (SCREENSIZE[0]/2-40, SCREENSIZE[1]/2-120))
        SCREEN.blit(title_font.render("You won!!", True, (255, 255, 0)), (300, 70))

        p.draw.rect(SCREEN, (255, 0, 0), close_button_rect)

        SCREEN.blit(close_text, (close_button_rect.x + 30, close_button_rect.y + 10))
        
        for event in p.event.get():
            if event.type == p.QUIT:
                game = False

            if event.type == p.MOUSEBUTTONDOWN:
                if close_button_rect.collidepoint(event.pos):
                    game = False
    
    elif menu_screen == 'game_over':
        SCREEN.fill((0, 0, 0))
        title_font = p.font.SysFont("Arial", 50)
        SCREEN.blit(title_font.render("GAME OVER", True, (255, 0, 0)), (230, 120))
        
        p.draw.rect(SCREEN, (0, 255, 0), play_button_rect)
        SCREEN.blit(title_font.render("Restart", True, (255, 255, 255)), (play_button_rect.x + 20, play_button_rect.y + 5))

        p.draw.rect(SCREEN, (255, 0, 0), close_button_rect)
        SCREEN.blit(close_text, (close_button_rect.x + 30, close_button_rect.y + 10))

        for event in p.event.get():
            if event.type == p.QUIT:
                game = False
            if event.type == p.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    lvl = 1
                    player.reset_stats()
                    start_lvl()
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

        if enemy_spawns: 
            level_started = True
        now = p.time.get_ticks()

        if enemy_spawns and (now - last_spawn_time > spawn_delay):
            last_spawn_time = now
            spawn = enemy_spawns.pop(0)
            
            if spawn["type"] == 3:
                new_v = WALK_ENEMY_V(spawn["x"], spawn["y"], W_RESOURCES, 2, spawn["y"] + 200)
                enemies.append(new_v)
                
            elif spawn["type"] == 4:
                new_h = WALK_ENEMY_H(spawn["x"], spawn["y"], W_RESOURCES, 2, spawn["x"] + 200)
                enemies.append(new_h)

            elif spawn["type"] == 5:
                new_s = SMART_ENEMY(spawn["x"], spawn["y"], S_RESOURCES, 1)
                enemies.append(new_s)

        for enemy in enemies:
            if isinstance(enemy, SMART_ENEMY):
                enemy.move((player.pos_x, player.pos_y), maps_obj)
                enemy.attack(enemy_bullets, player.rect, maps_obj)
            else:
                enemy.move()
                enemy.attack(enemy_bullets)
            enemy.draw_img()
            enemy.draw_hp()
            

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
                        wall.health -= player.damage
                        if wall.health <= 0: maps_obj.remove(wall)
                    explosions.append(EXPLOSION(b.x, b.y, EXPLOSION_FRAMES))
                    if b in bullets: bullets.remove(b)
                    break

            for enemy in enemies[:]:
                if b.rect.colliderect(enemy.rect):
                    enemy.take_damage(player.damage)
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

            if eb and eb.rect.colliderect(player.rect):
                explosions.append(EXPLOSION(player.pos_x, player.pos_y, EXPLOSION_FRAMES))
                enemy_bullets.remove(eb)
                is_dead = player.take_damage(20)
                if is_dead:
                    menu_screen = 'game_over'
            
            for wall in maps_obj[:]:
                if eb.rect.colliderect(wall.rect):
                    if not wall.indestructible:
                        wall.health -= 20
                        if wall.health <= 0: maps_obj.remove(wall)
                    explosions.append(EXPLOSION(eb.x, eb.y, EXPLOSION_FRAMES))
                    if eb in bullets: bullets.remove(b)
                    break
        
        for exp in explosions[:]:
            exp.update()
            if not exp.alive:
                explosions.remove(exp)
        for exp in explosions:
            exp.draw(SCREEN)

        if level_started and len(enemies) == 0 and len(enemy_spawns) == 0:
            lvl += 1
            if lvl <= len(LEVELES):
                start_lvl()
            else:
                menu_screen = 'win'

        for event in p.event.get():
            if event.type == p.QUIT:
                game = False
            if event.type == p.KEYDOWN:
                keys = p.key.get_pressed()
                if event.key == p.K_ESCAPE:
                    menu_screen = 'pause'
                if event.key == p.K_SPACE:
                    player.attack(bullets)
                if keys[p.K_LCTRL] and keys[p.K_LSHIFT] and event.key == p.K_g:
                    if keys[p.K_LCTRL] and keys[p.K_LSHIFT] and event.key == p.K_g:
                        player.god_mode = not player.god_mode
                        
                        if player.god_mode:
                            player.health = 1000000
                            player.max_health = 1000000
                            player.damage = 1000000
                            player.speed = 5
                            player.shoot_delay = 10
                            player.lives = 999999
                            logging.info("God Mode: ON")
                        else:
                            player.reset_stats()
                            logging.info("God Mode: OFF")


        now = p.time.get_ticks()
        if player.moving:
            if now - player.last_change > 300:
                player.last_change = now
                player.index = (player.index + 1) % len(player.frames)
                
                player.original_image = player.frames[player.index]
                player.image = p.transform.rotate(player.original_image, player.angle)
    p.display.update()
    clock.tick(FPS)


p.quit()