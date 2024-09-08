import random


def init_game() -> dict:
    """
        Initializes the game data structure.

        Returns:
            dict: A dictionary containing game settings, including the number of rows and columns,
                  player scores, the game board, and other necessary game state information.
    """
    rows, columns = 4, 4
    cards = ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'E', 'E', 'F', 'F', 'G', 'G', 'H', 'H']
    game_data = {
        'rows': rows,
        'columns': columns,
        'score': {'player1': 0, 'player2': 0},
        'turn': 'player1',
        'game_over': False,
        'board': prepare_board(rows, columns, cards),
        'move_history': []
    }
    return game_data


def prepare_board(rows, columns, cards) -> dict:
    """
        Prepares the game board by shuffling cards and placing them into the board structure.

        Args:
            rows (int): Number of rows in the board.
            columns (int): Number of columns in the board.
            cards (list): List of card values to be placed on the board.

        Returns:
            dict: A dictionary representing the game board, where each key is a tuple (row, col)
                  and the value is a dictionary with card information (card value, flipped state, matched state).
    """
    random.shuffle(cards)
    board = {}
    index = 0
    for r in range(rows):
        for c in range(columns):
            board[(r, c)] = {'card': cards[index], 'flipped': False, 'matched': False}
            index += 1
    return board


def flip_card(game_data, position) -> None:
    """
            Making sure the picked card is available and not flipped.

            Args:
                game_data : overall data of the game.
                position : the position of the picked card.

    """
    board = game_data['board']
    if board[position]['flipped'] or board[position]['matched']:
        print("Card already flipped or matched!")
    else:
        board[position]['flipped'] = True


def check_match(game_data, first_pos, second_pos) -> bool:
    """
            checking whether the picked cards are matched.

            Args:
                game_data : overall data of the game.
                first_pos : the first card picked
                second_pos : the second card picked

            Returns:
                bool: a boolean that let us know whether the cards are matching or not.
        """
    board = game_data['board']
    if board[first_pos]['card'] == board[second_pos]['card']:
        board[first_pos]['matched'] = True
        board[second_pos]['matched'] = True
        return True
    else:
        board[first_pos]['flipped'] = False
        board[second_pos]['flipped'] = False
        return False


def print_board(game_data) -> None:
    """
            displaying the board.

            Args:
                game_data : overall data of the game.

    """
    board = game_data['board']
    rows, columns = game_data['rows'], game_data['columns']
    for r in range(rows):
        row_display = []
        for c in range(columns):
            if board[(r, c)]['flipped'] or board[(r, c)]['matched']:
                row_display.append(board[(r, c)]['card'])
            else:
                row_display.append('X')
        print(' '.join(row_display))

    print()


def play(game_data) -> None:
    """
        Runs the main game loop, handling player turns, guessing, and score updates.

        Args:
            game_data (dict): The game data dictionary containing the board, scores, and other game information.
    """
    while not game_data['game_over']:
        current_player = game_data['turn']
        print(f"{current_player}'s turn!")
        has_found_match = True
        while has_found_match:
            print_board(game_data)
            first_pos = get_player_input(game_data)
            flip_card(game_data, first_pos)
            print_board(game_data)

            second_pos = get_player_input(game_data)
            flip_card(game_data, second_pos)
            print_board(game_data)

            if check_match(game_data, first_pos, second_pos):
                print(f"{current_player} found a match!")
                game_data['score'][current_player] += 1
                if all(card['matched'] for card in game_data['board'].values()):
                    game_data['game_over'] = True
                    print("Congratulations, the game is over!")
                    declare_winner(game_data)
                    return
            else:
                print(f"No match for {current_player}.")
                has_found_match = False
        game_data['turn'] = 'player2' if game_data['turn'] == 'player1' else 'player1'


def get_player_input(game_data) -> tuple:
    """
        gets the inputs from the user.

        Args:
            game_data : overall data of the game.

        Returns:
            tuple : returns a tuple of integers representing the row and column.
    """
    while True:
        try:
            user_input = input("Enter the position of the card (row,column): ")
            row, col = map(int, user_input.split(','))
            if (row, col) in game_data['board']:
                return row, col
            else:
                print("Invalid position. Try again.")
        except ValueError:
            print("Invalid input. Please enter row,column.")


def declare_winner(game_data) -> None:
    """
        Declaring the winner.

        Args:
            game_data : overall data of the game.

    """
    score1 = game_data['score']['player1']
    score2 = game_data['score']['player2']
    print(f"Final Scores - Player 1: {score1}, Player 2: {score2}")

    if score1 > score2:
        print("Player 1 wins!")
    elif score2 > score1:
        print("Player 2 wins!")
    else:
        print("It's a tie!")
