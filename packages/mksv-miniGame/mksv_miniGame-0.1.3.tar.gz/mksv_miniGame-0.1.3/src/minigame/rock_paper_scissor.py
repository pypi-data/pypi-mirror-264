import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors")

# colors
BLACK = (0, 0, 0) #background 
WHITE = (255, 255, 255) #text color 
LIGHT_GREEN = (144, 238, 144) # button color
DARK_GREEN = (0, 128, 0)  # button hover color

# fonts
font_big = pygame.font.SysFont(None, 43)
font_small = pygame.font.SysFont(None, 28)
font_button = pygame.font.SysFont(None, 32)

# center text
def center_text(text_surface, x, y):
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

#  draw button with centered text 
def draw_button(x, y, width, height, text, hover=False):
    button_rect = pygame.Rect(x, y, width, height)
    color = DARK_GREEN if button_rect.collidepoint(pygame.mouse.get_pos()) else LIGHT_GREEN  # check hover
    pygame.draw.rect(screen, color, button_rect)
    text_surface = font_button.render(text, True, BLACK)
    center_text(text_surface, x + width // 2, y + height // 2)
    return button_rect

# function to run the game (game loop)
def run_rps_game():
    global player_wins, computer_wins
    running = True
    clock = pygame.time.Clock()
    player_wins = 0
    computer_wins = 0
    result_message = ""
    play_again_button = None

    while running:
        screen.fill(BLACK)
        message = font_big.render(f"Player: {player_wins} | Computer: {computer_wins}", True, WHITE)
        center_text(message, WIDTH // 2, 75) # center score and make it 75 pixels from top of screen 
        center_text(font_small.render("Click on Rock, Paper, or Scissors", True, WHITE), WIDTH // 2, 125) #instructions at 125 pixels from top
        result = font_small.render(result_message, True, WHITE)
        center_text(result, WIDTH // 2, 400) # center result message and keep it 400 pixels from top of screen 

        # draw buttons at 200 pixels from top of screen 
        rock_button = draw_button(150, 200, 150, 50, "Rock")
        paper_button = draw_button(350, 200, 150, 50, "Paper")
        scissors_button = draw_button(550, 200, 150, 50, "Scissors")

        # if the game is over, display the "Play Again" button
        if player_wins >= 2 or computer_wins >= 2:
            play_again_button = draw_button(300, 300, 200, 50, "Play Again") 

        # get mouse position 
        mouse_position = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #if "Play again" button is on screen" and it is clicked, reset the game 
                if play_again_button is not None and play_again_button.collidepoint(mouse_position):
                    player_wins = 0
                    computer_wins = 0
                    result_message = ""
                    play_again_button = None  # reset the button
                elif not (player_wins >= 2 or computer_wins >= 2):  # only process button clicks if the game is not over
                    if rock_button.collidepoint(mouse_position):
                        result_message = play_round("Rock")
                    elif paper_button.collidepoint(mouse_position):
                        result_message = play_round("Paper")
                    elif scissors_button.collidepoint(mouse_position):
                        result_message = play_round("Scissors")

        pygame.display.flip()

# function to implement game functionality (score) and result messages displayed on the screen 
def play_round(player_choice):
    global player_wins, computer_wins
    computer_choice = random.choice(["Rock", "Paper", "Scissors"])
    result_message = f"You chose {player_choice}. Computer chose {computer_choice}. "

    if (player_choice == "Rock" and computer_choice == "Scissors") or \
       (player_choice == "Paper" and computer_choice == "Rock") or \
       (player_choice == "Scissors" and computer_choice == "Paper"):
        player_wins += 1
        if player_wins == 2:
            result_message += "You win the game! Congratulations!"
        else: 
            result_message += "You win this round!"
    elif player_choice == computer_choice:
        result_message += "It's a tie!"
    else:
        computer_wins += 1
        if computer_wins == 2: 
            result_message += "You lose! Computer wins the game!"
        else:
            result_message += "Computer wins this round!"
    
    return result_message


