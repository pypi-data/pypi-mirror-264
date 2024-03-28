def main():
    # offer choice for the user 
    print("Welcome to Game Selection!")
    print("Which game would you like to play?")
    print("1. Space Invaders")
    print("2. Count Game")
    print("3. Rock paper Scissors")
    print("4. Tic Tac Toe")

    choice = input("Enter the number of the game you want to play: ")

    # depending on selection --> present certain game 
    if choice == "1":
        from . import space_invaders as spacegame
        print("Welcome to Space Invaders Game!")
        spacegame.run_space_game()
    elif choice == "2":
        from . import count as countgame
        print("Welcome to Count Game!")
        countgame.run_count_game()
    elif choice == "3":
        from . import rock_paper_scissor as rpsgame
        print("Welcome to Rock Paper Scissors!")
        rpsgame.run_rps_game()
    elif choice == "4":
        from . import tictactoe as tttgame
        print("Welcome to Tic Tac Toe!")
        tttgame.run_tic_tac_toe()
    else:
        print("Invalid choice. Please enter either '1', '2', '3', or '4'.")

if __name__ == "__main__":
    main()
