import pygame
import os

WIDTH, HEIGHT = 700, 700
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 50
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
BORDER = pygame.Rect(0, HEIGHT - SPACESHIP_HEIGHT - 60, WIDTH, 5)
SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.jpeg')), (WIDTH, HEIGHT))

SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'player_ship.png'))
PLAYER_SHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(
    SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180)

def draw_window(player_ship, player_bullets):
    WINDOW.blit(SPACE, (0, 0))
    
    pygame.draw.rect(WINDOW, WHITE, BORDER) # to be removed later
    # pygame.draw.rect(WINDOW, RED, player_ship)
    WINDOW.blit(PLAYER_SHIP_IMAGE, (player_ship.x, player_ship.y))
    
    for bullet in player_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)
    
    pygame.display.update()
    
def handle_player_movement(keys_pressed, player_ship):
    if keys_pressed[pygame.K_a] and player_ship.x - VEL > 0:  # LEFT
        player_ship.x -= VEL
    if keys_pressed[pygame.K_d] and player_ship.x + VEL + player_ship.width < WIDTH:  # RIGHT
        player_ship.x += VEL
    # if keys_pressed[pygame.K_w] and player_ship.y - VEL > 0:  # UP
    #     player_ship.y -= VEL
    # if keys_pressed[pygame.K_s] and player_ship.y + VEL + player_ship.height < HEIGHT:  # DOWN
    #     player_ship.y += VEL
    
def handle_bullets(player_bullets, player_ship):
    for bullet in player_bullets:
        bullet.y -= BULLET_VEL
        if bullet.y < 0:
            player_bullets.remove(bullet)

def main():
    run = True
    player_ship = pygame.Rect(WIDTH//2 - SPACESHIP_WIDTH//2, HEIGHT - SPACESHIP_HEIGHT - 30, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    enemy_ship = pygame.Rect(WIDTH//2 - SPACESHIP_WIDTH//2, HEIGHT - SPACESHIP_HEIGHT - 30, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    player_bullets = []
    
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
        handle_enemy_movement(keys_pressed, enemy_ship)
        handle_bullets(player_bullets, player_ship)
        draw_window(player_ship, player_bullets)
        
    pygame.quit()

if __name__ == "__main__":
    main()
