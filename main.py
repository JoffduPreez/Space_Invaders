import pygame
import os

WIDTH, HEIGHT = 700, 700
ENEMY_AREA_WIDTH = 500
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 40, 40
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 30
VEL = 10
BULLET_VEL = 14
MAX_BULLETS = 3
ENEMY_SHIP_ROWS = 4
ENEMY_SHIPS_PER_ROW = 8
SPACE_BETWEEN_ROWS = 25
ENEMY_SPEED = 1

# 32 ships, every 5 ships killed add 1 to speed?

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
BORDER = pygame.Rect(0, HEIGHT - SPACESHIP_HEIGHT - 60, WIDTH, 5)
SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.jpeg')), (WIDTH, HEIGHT))

SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'player_ship.png'))
PLAYER_SHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(
    SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180)

ENEMY_IMAGE = pygame.image.load(
    os.path.join('Assets', 'enemy_ship.png'))
ENEMY_SHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(
    ENEMY_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180)

def draw_window(player_ship, player_bullets, enemy_ship_list):
    WINDOW.blit(SPACE, (0, 0))
    
    pygame.draw.rect(WINDOW, WHITE, BORDER) # to be removed later
    WINDOW.blit(PLAYER_SHIP_IMAGE, (player_ship.x, player_ship.y))
    
    for bullet in player_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)
        
    for enemy_ship_row in enemy_ship_list:
        for ship in enemy_ship_row:
            # pygame.draw.rect(WINDOW, RED, ship)
            WINDOW.blit(ENEMY_SHIP_IMAGE, (ship.x, ship.y))
    
    pygame.display.update()
    
def handle_player_movement(keys_pressed, player_ship):
    if keys_pressed[pygame.K_a] and player_ship.x - VEL > 0:  # LEFT
        player_ship.x -= VEL
    if keys_pressed[pygame.K_d] and player_ship.x + VEL + player_ship.width < WIDTH:  # RIGHT
        player_ship.x += VEL

def handle_enemy_movement(enemy_ship_list, enemy_direction):
    for enemy_ship_row in enemy_ship_list:
        for ship in enemy_ship_row:
            if ship.x + ENEMY_SPEED + SPACESHIP_WIDTH >= WIDTH:
                # print(str(ship.x + ENEMY_SPEED) + " < " + str(WIDTH))
                enemy_direction = "left"
                shift_enemy_down(enemy_ship_list)
            if ship.x - ENEMY_SPEED <= 0:
                enemy_direction = "right"
                shift_enemy_down(enemy_ship_list)

            if enemy_direction == "right":
                ship.x += ENEMY_SPEED
            elif enemy_direction == "left":
                ship.x -= ENEMY_SPEED
    return enemy_direction

def shift_enemy_down(enemy_ship_list):
    for enemy_ship_row in enemy_ship_list:
        for ship in enemy_ship_row:
            ship.y += (SPACESHIP_HEIGHT - SPACE_BETWEEN_ROWS)
    
def handle_bullets(player_bullets, player_ship, enemy_ship_list, kill_count):
    global ENEMY_SPEED
    
    for bullet in player_bullets:
        bullet.y -= BULLET_VEL
        if bullet.y < 0:
            player_bullets.remove(bullet)
        
        for enemy_ship_row in enemy_ship_list:
            for ship in enemy_ship_row:        
                if ship.colliderect(bullet):
                    enemy_ship_row.remove(ship)
                    player_bullets.remove(bullet)
                    kill_count += 1
                    if kill_count % 5 == 0:
                        ENEMY_SPEED += 1   
    return kill_count

def main():
    enemy_direction = "right"
    run = True
    kill_count = 0
    player_ship = pygame.Rect(WIDTH//2 - SPACESHIP_WIDTH//2, HEIGHT - SPACESHIP_HEIGHT - 30, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    player_bullets = []
    
    space_taken_by_ships = ENEMY_SHIPS_PER_ROW * SPACESHIP_WIDTH
    space_to_fill = ENEMY_AREA_WIDTH - space_taken_by_ships
    space_between_ships = space_to_fill//(ENEMY_SHIPS_PER_ROW+1)
    
    difference = (WIDTH - ENEMY_AREA_WIDTH) // 2
    
    enemy_ship_list = [
        [pygame.Rect(difference + space_between_ships, SPACE_BETWEEN_ROWS, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)],
        [pygame.Rect(difference + space_between_ships, SPACE_BETWEEN_ROWS * 2 + SPACESHIP_HEIGHT, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)],
        [pygame.Rect(difference + space_between_ships, SPACE_BETWEEN_ROWS * 3 + SPACESHIP_HEIGHT * 2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)],
        [pygame.Rect(difference + space_between_ships, SPACE_BETWEEN_ROWS * 4 + SPACESHIP_HEIGHT * 3, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)]]
        
    left_distance_placeholder = difference + space_between_ships + SPACESHIP_WIDTH + space_between_ships
    top_distance_placeholder = SPACE_BETWEEN_ROWS
            
    for i in range(0, ENEMY_SHIP_ROWS):
        for j in range(1,ENEMY_SHIPS_PER_ROW):
            # print("[" + str(i) + "]" + "[" + str(j) + "]")
            enemy_ship_list[i].append(pygame.Rect(left_distance_placeholder, top_distance_placeholder, SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
            left_distance_placeholder += SPACESHIP_WIDTH
            left_distance_placeholder += space_between_ships
        top_distance_placeholder += SPACESHIP_HEIGHT
        top_distance_placeholder += SPACE_BETWEEN_ROWS
        left_distance_placeholder = difference + space_between_ships + SPACESHIP_WIDTH + space_between_ships

    
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(player_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        player_ship.x + player_ship.width//2 - 2, player_ship.y, 5, 10)
                    player_bullets.append(bullet)
                    #BULLET_FIRE_SOUND.play()
        
        keys_pressed = pygame.key.get_pressed()
        handle_player_movement(keys_pressed, player_ship)
        enemy_direction = handle_enemy_movement(enemy_ship_list, enemy_direction)
        kill_count = handle_bullets(player_bullets, player_ship, enemy_ship_list, kill_count)
        draw_window(player_ship, player_bullets, enemy_ship_list)
        
    pygame.quit()

if __name__ == "__main__":
    main()
