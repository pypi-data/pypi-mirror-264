import pygame
import sys
import random
import time

#functions
enemies = []
def spawn_enemy():
    x = random.randint(0, screen_width - enemy_size)
    y = -enemy_size # Start enemies above the screen
    enemies.append([x, y])
    return enemies

player_size = 50
def draw_player(x, y):
    pygame.draw.rect(screen, PLAYER_COLOR, (x, y, player_size, player_size))

enemy_size = 40
def draw_enemy(x, y):
    pygame.draw.rect(screen, ENEMY_COLOR, (x, y, enemy_size, enemy_size))
    
def draw_bullet(x, y):
    pygame.draw.rect(screen, BULLET_COLOR, (x, y, 5, 10))
  

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders")

# Define colors
BACKGROUND_COLOR = (0, 0, 0)
PLAYER_COLOR = (0, 255, 0)
ENEMY_COLOR = (255, 0, 0)
BULLET_COLOR = (0, 0, 255)

# main game
def run_space_game():
    pygame.init()  

    font = pygame.font.SysFont(None, 40)
    clock = pygame.time.Clock()

    game_active = True
    score = 0

    #game variables
    player_x = screen_width // 2 - player_size // 2
    player_y = screen_height - 100
    player_speed = 5
    enemy_speed = 3.5
    enemy_cooldown = 25  # Number of frames between enemy spawns
    enemy_last_spawn = 0
    bullets = []
    bullet_speed = 7

    def show_score(score):
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

    def game_over():
        global game_active
        game_active = False
        screen.fill(BACKGROUND_COLOR)
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        screen.blit(game_over_text, (screen_width // 2 - 100, screen_height // 2 - 50))
        final_score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
        screen.blit(final_score_text, (screen_width // 2 - 130, screen_height // 2 + 50))
        pygame.display.flip()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    def game_win():
        global game_active
        game_active = False
        screen.fill(BACKGROUND_COLOR)
        game_win_text = font.render("Game Win", True, (255, 255, 255))
        screen.blit(game_win_text, (screen_width // 2 - 80, screen_height // 2 - 20))
        pygame.display.flip()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    # instructions for the game 
    font = pygame.font.SysFont(None, 60)
    intro_text = font.render("Space Invaders", True, (255, 255, 255))

    font = pygame.font.SysFont(None, 35)
    screen.blit(intro_text, (screen_width // 2 - 170, screen_height // 2 - 120))
    instruc_text = font.render("move with L/R arrow keys", True, (255, 255, 255))
    screen.blit(instruc_text, (screen_width // 2 -160, screen_height // 2 -40))
    instruc_text2 = font.render("press space to shoot", True, (255, 255, 255))
    screen.blit(instruc_text2, (screen_width // 2-125, screen_height // 2 -10))

    font = pygame.font.SysFont(None, 40)
    point_text = font.render("GET 20 POINTS TO WIN", True, (255, 255, 255))
    screen.blit(point_text, (screen_width // 2-170, screen_height // 2 + 60))
    pygame.display.flip()
    time.sleep(4)

    # main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append([player_x + player_size // 2 - 2, player_y])

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_size:
            player_x += player_speed

        # enemies spawn
        if game_active:
            if enemy_last_spawn == 0:
                spawn_enemy()
                enemy_last_spawn = enemy_cooldown
            else:
                enemy_last_spawn -= 1

        # enemy speed
        for enemy in enemies:
            enemy[1] += enemy_speed

        #move bullets
        for bullet in bullets:
            bullet[1] -= bullet_speed
            for enemy in enemies:
                if (bullet[0] > enemy[0] and bullet[0] < enemy[0] + enemy_size and
                    bullet[1] > enemy[1] and bullet[1] < enemy[1] + enemy_size):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1
                    break 

        # check for collisions
        for enemy in enemies:
            if enemy[1] > screen_height:
                enemies.remove(enemy)
                #score += 1
            elif (player_x < enemy[0] + enemy_size and
                  player_x + player_size > enemy[0] and
                  player_y < enemy[1] + enemy_size and
                  player_y + player_size > enemy[1]):
                game_over()

        # if certain points --> win 
        if score == 20:
            game_win()

        # draw everything (enemy, user, bullets)
        screen.fill(BACKGROUND_COLOR)
        draw_player(player_x, player_y)
        for enemy in enemies:
            draw_enemy(enemy[0], enemy[1])
        for bullet in bullets:
            draw_bullet(bullet[0], bullet[1])
        show_score(score)
        pygame.display.flip()
        clock.tick(60)
