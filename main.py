import pygame
import random
import os
pygame.font.init()

WIDTH, HEIGHT = 700, 700
ENEMY_AREA_WIDTH = 500
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 40, 40
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
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
PLAYER_HIT = pygame.USEREVENT + 1
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)

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


def draw_window(player_ship, player_bullets, enemy_ship_list, enemy_bullets, player_health):
    WINDOW.blit(SPACE, (0, 0))
    
    pygame.draw.rect(WINDOW, WHITE, BORDER) # to be removed later
    WINDOW.blit(PLAYER_SHIP_IMAGE, (player_ship.x, player_ship.y))
    
    for bullet in player_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet)

    for bullet in enemy_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)
        
    player_health_text = HEALTH_FONT.render(
        "Health: " + str(player_health), 1, WHITE)
    WINDOW.blit(player_health_text, (10, 10))
        
    index = 0
    for enemy_ship_row in enemy_ship_list:
        index = 0
        for ship in enemy_ship_row:
            # pygame.draw.rect(WINDOW, RED, ship)
            if enemy_ship_row[index] != 0:
                WINDOW.blit(ENEMY_SHIP_IMAGE, (ship.x, ship.y))
            index += 1
    
    pygame.display.update()
    
def create_enemy_ships():
    space_taken_by_ships = ENEMY_SHIPS_PER_ROW * SPACESHIP_WIDTH
    space_to_fill = ENEMY_AREA_WIDTH - space_taken_by_ships
    space_between_ships = space_to_fill//(ENEMY_SHIPS_PER_ROW+1)
    difference = (WIDTH - ENEMY_AREA_WIDTH) // 2
    
    # initialize the 2D array of enemy ships
    enemy_ship_list = [
        [pygame.Rect(difference + space_between_ships, SPACE_BETWEEN_ROWS, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)],
        [pygame.Rect(difference + space_between_ships, SPACE_BETWEEN_ROWS * 2 + SPACESHIP_HEIGHT, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)],
        [pygame.Rect(difference + space_between_ships, SPACE_BETWEEN_ROWS * 3 + SPACESHIP_HEIGHT * 2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)],
        [pygame.Rect(difference + space_between_ships, SPACE_BETWEEN_ROWS * 4 + SPACESHIP_HEIGHT * 3, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)]]
    
        # used to determine where to position the enemy ships
    left_distance_placeholder = difference + space_between_ships + SPACESHIP_WIDTH + space_between_ships
    top_distance_placeholder = SPACE_BETWEEN_ROWS
    
    # populate the 2D array of enemy ships
    for i in range(0, ENEMY_SHIP_ROWS):
        for j in range(1,ENEMY_SHIPS_PER_ROW):
            enemy_ship_list[i].append(pygame.Rect(left_distance_placeholder, top_distance_placeholder, SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
            left_distance_placeholder += SPACESHIP_WIDTH
            left_distance_placeholder += space_between_ships
        top_distance_placeholder += SPACESHIP_HEIGHT
        top_distance_placeholder += SPACE_BETWEEN_ROWS
        left_distance_placeholder = difference + space_between_ships + SPACESHIP_WIDTH + space_between_ships
        
    return enemy_ship_list
        
    
def handle_player_movement(keys_pressed, player_ship):
    if keys_pressed[pygame.K_a] and player_ship.x - VEL > 0:  # LEFT
        player_ship.x -= VEL
    if keys_pressed[pygame.K_d] and player_ship.x + VEL + player_ship.width < WIDTH:  # RIGHT
        player_ship.x += VEL


def handle_enemy_movement(enemy_ship_list, enemy_direction):
    index = 0
    for enemy_ship_row in enemy_ship_list:
        index = 0
        for ship in enemy_ship_row:
            if enemy_direction == "right" and enemy_ship_row[index] != 0:
                ship.x += ENEMY_SPEED
            elif enemy_direction == "left" and enemy_ship_row[index] != 0:
                ship.x -= ENEMY_SPEED
            index += 1

    # need to have two separate loops, otherwise it messes up the positon of enemy ships
    for enemy_ship_row in enemy_ship_list:
        index = 0
        for ship in enemy_ship_row:
            if enemy_ship_row[index] != 0:
                if ship.x + SPACESHIP_WIDTH >= WIDTH:
                    enemy_direction = "left"
                    shift_enemy_down(enemy_ship_list)
                if ship.x <= 0:
                    enemy_direction = "right"
                    shift_enemy_down(enemy_ship_list)
            index += 1

    return enemy_direction


def shift_enemy_down(enemy_ship_list):
    index = 0
    for enemy_ship_row in enemy_ship_list:
        index = 0
        for ship in enemy_ship_row:
            if enemy_ship_row[index] != 0:
                ship.y += (SPACESHIP_HEIGHT - SPACE_BETWEEN_ROWS)
            index += 1
            
def print_enemy_ships(enemy_ship_list):
    i = 0
    for enemy_ship_row in enemy_ship_list:
        for ship in enemy_ship_row:
            print(str(i) + " ", end = ' ')
            i += 1


def generate_enemy_bullet(enemy_ship_list, front_ships_list, enemy_bullets):
    column_to_shoot = random.randrange(0, ENEMY_SHIPS_PER_ROW)
    row_to_shoot = front_ships_list[column_to_shoot]
    
    while enemy_ship_list[row_to_shoot][column_to_shoot] == 0:
        column_to_shoot = random.randrange(0, ENEMY_SHIPS_PER_ROW)
        row_to_shoot = front_ships_list[column_to_shoot]
        
    ship = enemy_ship_list[row_to_shoot][column_to_shoot]
    bullet = pygame.Rect(ship.x + ship.width//2 - 2, ship.y, 5, 10)
    enemy_bullets.append(bullet)
    
    # i just realized, i am not accounting for the ships that have been shot when i do column_to_shoot
    # for example if the front row has had 3 ships shot down, column_to_shoot should be randomized from 0 - however many ships are left, not from 0 - ENEMY_SHIPS_PER_ROW
    # at the same time, if we want to shoot from the second last ship, then we would do column 7 (assuming 8 columns). This would be index 6. But if the front row has had 3 ships shot down, then we actually need to do index 3. Thus, we need to keep track of how many ships have been shot down per row
    

def handle_bullets(player_bullets, player_ship, enemy_ship_list, kill_count, front_ships_list):
    global ENEMY_SPEED
    
    for bullet in player_bullets:
        bullet.y -= BULLET_VEL
        if bullet.y < 0:
            player_bullets.remove(bullet)
        
        # this variable just keeps track of what index i need to access front_ships_list at
        index = 0
        for enemy_ship_row in enemy_ship_list:
            index = 0
            for ship in enemy_ship_row:
                if enemy_ship_row[index] != 0 and ship.colliderect(bullet):
                    front_ships_list[index] -= 1
                    print(front_ships_list)
                    
                    enemy_ship_row[index] = 0
                    player_bullets.remove(bullet)
                    kill_count += 1
                    
                    if kill_count % 5 == 0:
                        ENEMY_SPEED += 1
                index += 1

    return kill_count


def handle_enemy_bullets(enemy_bullets, player_ship):
    for bullet in enemy_bullets:
        bullet.y += BULLET_VEL
        if bullet.y > HEIGHT:
            enemy_bullets.remove(bullet)
        if player_ship.colliderect(bullet):
            enemy_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(PLAYER_HIT))


def main():
    enemy_direction = "right"
    run = True
    kill_count = 0
    player_bullets = []
    enemy_bullets = []
    player_health = 3
    player_ship = pygame.Rect(WIDTH//2 - SPACESHIP_WIDTH//2, HEIGHT - SPACESHIP_HEIGHT - 30, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    enemy_ship_list = create_enemy_ships()
    front_ships_list = [] # this array records what row the closest ship is to the player for each column
    enemy_shoot_timer = 0
    
    for i in range(0, ENEMY_SHIPS_PER_ROW):
        front_ships_list.append(ENEMY_SHIP_ROWS-1)    

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
            if event.type == PLAYER_HIT:
                player_health -= 1
                    
        keys_pressed = pygame.key.get_pressed()
        handle_player_movement(keys_pressed, player_ship)
        enemy_direction = handle_enemy_movement(enemy_ship_list, enemy_direction)
        kill_count = handle_bullets(player_bullets, player_ship, enemy_ship_list, kill_count, front_ships_list)
        
        # deal with the generation and movement of enemy bullets
        enemy_shoot_timer += 1
        if enemy_shoot_timer == FPS:
            enemy_shoot_timer = 0
            generate_enemy_bullet(enemy_ship_list, front_ships_list, enemy_bullets)
        handle_enemy_bullets(enemy_bullets, player_ship)
        
        draw_window(player_ship, player_bullets, enemy_ship_list, enemy_bullets, player_health)
        
    pygame.quit()

if __name__ == "__main__":
    main()
