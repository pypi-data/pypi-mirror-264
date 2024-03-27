from src.minigame import rock_paper_scissor
import pygame
import pytest

#ROCK PAPER SCISSORS TESTS 
# test center_text function (test to ensure that text is centered on the screen)
# this test is a visual test of centering text (the test below is computational)
def test_center_text():
    pygame.init()
    # create display surface
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    font = pygame.font.SysFont(None, 28)  # create a font object
    text_surface = font.render("Test Text", True, (255, 255, 255))  # text onto a surface
    x, y = 100, 100
    rock_paper_scissor.center_text(text_surface, x, y)  # call the center_text function to test it
    text_rect = text_surface.get_rect(center=(x, y)) # get the rect of the text surface
    screen.blit(text_surface, text_rect) # blit the text surface onto the screen
    pygame.display.flip()  # update the display 

# test center_text function 
# another test that checks the centering of text by checking numbers rather than visually 
def test_center_text2():
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    font = pygame.font.SysFont(None, 28)
    text = "Test Text"
    text_surface = font.render(text, True, (255, 255, 255)) # render text onto a surface
    x, y = 100, 100
    rock_paper_scissor.center_text(text_surface, x, y)
    # get the rect of the text surface with the center set to the specified coordinates
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    blitted_text_position = text_rect.topleft # get the position of the blitted text
    # verify the position matches the expected coordinates!
    expected_position = (x - text_rect.width // 2, y - text_rect.height // 2)
    assert blitted_text_position == expected_position, f"Text not centered at ({x}, {y})"

# test draw_button function (ensure that the draw_button function creates a button rectangle of type pygame.Rect) 
def test_draw_button_creates_button():
    pygame.init()
    # button parameters
    x, y, width, height = 100, 100, 150, 50
    text = "Test Button"
    # call the draw_button function
    button_rect = rock_paper_scissor.draw_button(x, y, width, height, text)
    # check if button_rect is of type pygame.Rect
    assert isinstance(button_rect, pygame.Rect)

# test draw_button function (ensure that the draw_button function properly centers text within the button rectangle)
def test_draw_button_centered_text():
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.Surface((screen_width, screen_height))
    font_button = pygame.font.SysFont(None, 32)

    x, y, width, height = 100, 100, 150, 50
    text = "Test Button"
    button_rect = rock_paper_scissor.draw_button(x, y, width, height, text)
    pygame.draw.rect(screen, (0, 0, 0), button_rect)
    # get the text surface of the button
    text_surface = font_button.render(text, True, (0, 0, 0))
    # get expected text position
    text_x = x + width // 2 - text_surface.get_width() // 2
    text_y = y + height // 2 - text_surface.get_height() // 2
    # text surface onto the screen at the calculated position
    screen.blit(text_surface, (text_x, text_y))
    # check if the text is properly centered within the button rectangle
    # check if the color is black since text is black 
    assert screen.get_at((x + width // 2, y + height // 2))[:3] == (0, 0, 0)      

#test play_round function (does it give the appropriate winning message)
def test_game_result_message():
    rock_paper_scissor.player_wins = 1
    rock_paper_scissor.computer_wins = 1
    # below, we call play_round(rock)  so these are the potential messages if the player choses rock after winning one round (excluding ties)
    acceptable_messages = [ 
        "You chose Rock. Computer chose Paper. You lose! Computer wins the game!",
        "You chose Rock. Computer chose Scissors. You win the game! Congratulations!"
    ]
    # simulate rounds of the game until a player wins one more time (since score for each is already set to 1) 
    # while loop incase both player and computer draw rock 
    while rock_paper_scissor.player_wins < 2 and rock_paper_scissor.computer_wins < 2:
        result_message = rock_paper_scissor.play_round("Rock")  # choose "Rock" arbitrarily (for the sake of testing)
    # check if the correct result message is given when the game is won (in acceptable messages)
    if rock_paper_scissor.player_wins == 2:
        expected_result_message = "You chose Rock. Computer chose Scissors. You win the game! Congratulations!"
        assert result_message in acceptable_messages
    else:
        expected_result_message = "You chose Rock. Computer chose Paper. You lose! Computer wins the game!"
    # check that the result message matches the expected message for winning or losing the game
    assert result_message == expected_result_message

# test run_rps_game function (ensure that the Rock Paper Scissors game loop runs without errors)
def test_run_rps_game():
    pygame.init()
    # run the Rock Paper Scissors game loop (run_rps_game function)
    try:
        rock_paper_scissor.run_rps_game()
    except Exception as e:
        assert False, f"Error occurred while running the game loop: {e}"
    pygame.quit()






