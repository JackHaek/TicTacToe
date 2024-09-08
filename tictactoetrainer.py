from __future__ import annotations
import random
from typing import Final
import numpy as np
from numpy import ndarray
from tictactoe import TicTacToe


def _initialize_weights():
    mu, sigma = 0, 0.1
    rng = np.random.default_rng()
    s = rng.normal(mu, sigma, 9)
    return s


class TicTacToeTrainer:
    def __init__(self):
        self.board: TicTacToe = None
        self.weights = _initialize_weights()

    def _select_location_input(self, player) -> int | None:
        rtn_val = None
        input_accepted = False
        while not input_accepted:
            try:
                loc = input(f"It is player {player}'s turn! Select where you would like to go\n")
                rtn_val = self.board.make_move(player, int(loc))
                input_accepted = True
            except ValueError:
                print("That was not a valid move! Please enter a valid index 0 through 8 that is not occupied")
        return rtn_val

    def _check_game_condition(self, gc, print_non_winner = True) -> bool:
        if gc == 0:
            print("The Game was a draw!")
            print(self.board)
            return True
        elif gc == 1:
            print("Player X won the Game!")
            print(self.board)
            return True
        elif gc == -1:
            print("Player O won the Game!")
            print(self.board)
            return True
        else:
            if print_non_winner:
                print(f"The Current Board is:")
                print(self.board)
            return False

    def _ai_determine_next_move(self) -> int:
        pass

    def _algorithm_determine_next_move(self) -> int:
        state: Final[ndarray] = self.board.get_current_game_state()

        # If there is 2 values of the same in a row, no matter what team it is, the algorithm
        # should go there
        for idx, row in enumerate(state):
            vals, count = np.unique(row, return_counts=True)
            zipped = dict(zip(vals, count))
            #If there is an empty space and 2 of the same value
            if 0 in row and 2 in count and zipped[0] != 2:
                return int(np.where(row == 0)[0]) + (3 * idx)

        # If there is 2 values of the same in a column, no matter what team it is, the algorithm
        # should go there
        for col in range(3):
            column = state[:, col]
            vals, count = np.unique(column, return_counts=True)
            zipped = dict(zip(vals, count))
            if 0 in column and 2 in count and zipped[0] != 2:
                return col + int(np.where(column == 0)[0] * 3)

        # If there is 2 values of the same in a diagonal, no matter what team it is, the algorithm
        # should go there
        diagonals = [np.array([state[0][0], state[1][1], state[2][2]]), np.array([state[0][2], state[1][1], state[2][0]])]
        for idx, diagonal in enumerate(diagonals):
            vals, count = np.unique(diagonal, return_counts=True)
            zipped = dict(zip(vals, count))
            if 0 in diagonal and 2 in count and zipped[0] != 2:
                if idx == 0:
                    return 4 * int(np.where(diagonal == 0)[0])
                else:
                    return 2 + int(np.where(diagonal == 0)[0] * 2)

        # If none of these conditions exist, pick one at random
        avail_spaces = []
        for y in range(3):
            for x in range(3):
                if state[y][x] == 0:
                    avail_spaces.append((y*3) + x)

        return avail_spaces[random.randrange(0, len(avail_spaces))]

    def _determine_next_move(self, method) -> int:
        if method == "algorithm":
            return self._algorithm_determine_next_move()
        elif method == "ai":
            return self._ai_determine_next_move()

    def play_single_player(self):
        player_letter = None
        while not player_letter:
            possible_player_letter = input("Please choose a player: (X or O)\n")
            if possible_player_letter.upper() == "X":
                player_letter = "X"
            elif possible_player_letter.upper() == "O":
                player_letter = "O"
            else:
                print("Please provide a valid player (Either X or O)")

        method_select = None
        while not method_select:
            possible_method_select = input("Please choose a method: (ai or alg)\n")
            if possible_method_select.lower() == "alg":
                method_select = "algorithm"
            elif possible_method_select.lower() == "ai":
                method_select = "ai"
            else:
                print("Please provide a valid method (Either ai or alg)")

        print("Hello, welcome to TicTacToe")
        print("The placement indices are numbered from 0 to 8 and read left to right")

        self.board = TicTacToe()
        show_results = True
        game_is_over = False
        game_condition = None
        while not game_is_over:

            game_is_over = self._check_game_condition(game_condition, show_results)

            if self.board.get_active_player() == player_letter and not game_is_over:
                game_condition = self._select_location_input(self.board.get_active_player())
                show_results = False
            elif self.board.get_active_player() != player_letter and not game_is_over:
                game_condition = self.board.make_move(self.board.get_active_player(),
                                                      self._determine_next_move(method_select))
                show_results = True


    def play_multiplayer(self):
        print("Hello, welcome to TicTacToe")
        print("The placement indices are numbered from 0 to 8 and read left to right")

        self.board = TicTacToe()

        game_is_over = False
        game_condition = None
        while not game_is_over:

            game_is_over = self._check_game_condition(game_condition)

            if not game_is_over:
                current_player = self.board.get_active_player()
                game_condition = self._select_location_input(current_player)

    def train(self, iterations = 10000):
        pass