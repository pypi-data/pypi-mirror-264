import pygame
from pathlib import Path
import sys

current_dir = Path(__file__).parent


pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Tic Tac Toe")

BACKGROUND_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)


ttt_o_path = current_dir / 'ttt_o.png'
ttt_x_path = current_dir / 'ttt_x.png'

ttt_o = pygame.image.load(str(ttt_o_path))
ttt_o = pygame.transform.scale(ttt_o, (200, 200))
ttt_x = pygame.image.load(str(ttt_x_path))
ttt_x = pygame.transform.scale(ttt_x, (200, 200))


board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
player = 1
game_won = False
winner = 0
game_tie = False

def draw_lines():
    pygame.draw.line(screen, LINE_COLOR, (0, 200), (800, 200), 10)
    pygame.draw.line(screen, LINE_COLOR, (0, 400), (800, 400), 10)
    pygame.draw.line(screen, LINE_COLOR, (200, 0), (200, 600), 10)
    pygame.draw.line(screen, LINE_COLOR, (400, 0), (400, 600), 10)

def draw_figures():
    for row in range(3):
        for col in range(3):
            if board[row][col] == 1:
                screen.blit(ttt_x, (col * 200, row * 200))
            elif board[row][col] == 2:
                screen.blit(ttt_o, (col * 200, row * 200))

def center_text(text_surface, x, y):
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def check_winner():
    global game_won
    global winner
    global game_tie

    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != 0:
            winner = board[row][0]
            game_won = True
            return
        
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != 0:
            winner = board[0][col]
            game_won = True
            return
        
    if board[0][0] == board[1][1] == board[2][2] != 0:
        winner = board[0][0]
        game_won = True
        return
    
    if board[0][2] == board[1][1] == board[2][0] != 0:
        winner = board[0][2]
        game_won = True
        return
    
    if all([cell != 0 for row in board for cell in row]):
        game_tie = True
        return

def run_tic_tac_toe():
    global player
    global game_won
    global winner
    global game_tie

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_won and not game_tie:
                x, y = pygame.mouse.get_pos()
                row = y // 200
                col = x // 200

                if board[row][col] == 0:
                    board[row][col] = player
                    player = 1 if player == 2 else 2
            check_winner()


        screen.fill(BACKGROUND_COLOR)
        draw_lines()
        draw_figures()

        if game_won:
            if winner == 1:
                screen.fill(BACKGROUND_COLOR)
                message = "Player 1 wins!"
            else:
                screen.fill(BACKGROUND_COLOR)
                message = "Player 2 wins!"
            center_text(pygame.font.Font(None, 64).render(message, True, (0, 0, 0)), 300, 300)
        elif game_tie:
            screen.fill(BACKGROUND_COLOR)
            message = "It's a tie!"
            center_text(pygame.font.Font(None, 64).render(message, True, (0, 0, 0)), 300, 300)

        pygame.display.flip()
        pygame.display.update()
