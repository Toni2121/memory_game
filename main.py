import memory_game


if __name__ == "__main__":
    print("Welcome to the Memory Game!")
    game_data = memory_game.init_game()
    memory_game.play(game_data)
