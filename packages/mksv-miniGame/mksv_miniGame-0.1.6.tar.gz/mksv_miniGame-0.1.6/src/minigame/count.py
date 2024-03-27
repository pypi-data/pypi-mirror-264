import pygame
import sys
import random
import time

def draw_input_box(screen,font,text_color,text, rect, color=(255, 255, 255)):
    input_rect = pygame.Rect(rect)
    pygame.draw.rect(screen, color, input_rect, 2)
    text_surf = font.render(text, True, text_color)
    screen.blit(text_surf, (input_rect.x + 5, input_rect.y + 5))

def get_player_count(show_message,screen,background_color,font,screen_width,screen_height,text_color,clock):
    input_text = ''
    input_box_active = True

    while input_box_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and input_text:
                    input_box_active = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key in range(pygame.K_0, pygame.K_9 + 1) or event.key in range(pygame.K_KP0, pygame.K_KP9 + 1):
                    input_text += event.unicode

        screen.fill(background_color)
        question_text = "How many circles in total?"
        show_message(question_text, (screen_width // 2, screen_height // 3 - 50)) 
        draw_input_box(screen,font, text_color, input_text, (screen_width // 4, screen_height // 3, screen_width // 2, 50))
        pygame.display.flip()
        clock.tick(60)

    return int(input_text) if input_text.isdigit() else 0

def generate_objects(screen_width,screen_height):
    num_objects = random.randint(1, 4)
    circles = []
    radius = 30
    for _ in range(num_objects):
        overlapping = True
        while overlapping:
            overlapping = False
            x, y = random.randint(radius, screen_width - radius), random.randint(radius, screen_height - radius)
            for circle in circles:
                dx, dy = circle[0] - x, circle[1] - y
                if (dx**2 + dy**2)**0.5 < 2 * radius:
                    overlapping = True
                    break
            if not overlapping:
                circles.append((x, y))
    return circles

def show_count(screen, font, text_color,actual_count, player_count):
    player_count_surf = font.render(f'Your Count: {player_count}', True, text_color)
    screen.blit(player_count_surf, (10, 10))
    actual_count_surf = font.render(f'Actual Count: {actual_count}', True, text_color)
    screen.blit(actual_count_surf, (10, 60))

def run_count_game():
    pygame.init()

    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Flash Count Game")

    background_color = (30, 30, 30)
    object_color = (250, 50, 50)
    text_color = (255, 255, 255)
    button_color, button_hover_color = (0, 255, 0), (0, 200, 0)

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 55)

    game_active = False
    actual_count = 0
    start_time = 0

    
    def show_message(message, position, font_size=55):
        msg_font = pygame.font.SysFont(None, font_size)
        msg_surf = msg_font.render(message, True, text_color)
        msg_rect = msg_surf.get_rect(center=position)
        screen.blit(msg_surf, msg_rect)

    def draw_button(text, rect, action=None):
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        button_rect = pygame.Rect(rect)
        color = button_hover_color if button_rect.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(screen, color, button_rect)
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=button_rect.center)
        screen.blit(text_surf, text_rect)
        if button_rect.collidepoint(mouse_pos) and click[0] == 1 and action is not None:
            time.sleep(0.2)
            action()

    def reset_game():
        nonlocal game_active, actual_count, start_time
        game_active = True
        actual_count = 0
        start_time = time.time()

    def game_start():
        reset_game()
        main_game_loop()

    def title_screen():
        nonlocal game_active
        game_active = False
        while not game_active:
            screen.fill(background_color)
            show_message("Flash Count Game", (screen_width // 2, screen_height // 2 - 100), 65)
            draw_button("Start Game", (screen_width // 2 - 150, screen_height // 2, 300, 50), game_start)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.flip()
            clock.tick(60)

    def end_screen(actual_count):
        player_count = get_player_count(show_message,screen,background_color,font,screen_width,screen_height,text_color,clock)
        while True:
            screen.fill(background_color)
            correct_message = "Correct!" if actual_count == player_count else "Wrong!"
            show_message(correct_message, (screen_width // 2, screen_height // 2))
            show_count(screen,font,text_color,actual_count, player_count)

            draw_button("Play Again", (100, screen_height // 2 + 100, 200, 50), game_start)
            draw_button("Exit", (500, screen_height // 2 + 100, 200, 50), pygame.quit)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            clock.tick(60)

    def main_game_loop():
        nonlocal game_active, actual_count, start_time
        game_active = True
        while game_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill(background_color)
            actual_objects = generate_objects(screen_width,screen_height)
            actual_count += len(actual_objects)
            for circle in actual_objects:
                pygame.draw.circle(screen, object_color, circle, 30)

            pygame.display.flip()
            pygame.time.wait(1000)  # frequency

            if time.time() - start_time > 10: #duration
                game_active = False

        end_screen(actual_count)

    title_screen()


